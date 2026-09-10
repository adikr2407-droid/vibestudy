from database import get_db

def calculate_compatibility(user_profile, candidate):
    """
    Calculates compatibility points between user and candidate based on:
    - Schedule Match (+40 pts if time_pref matches exactly)
    - Target GPA Alignment (+30 pts max, penalizing 10 points per 1.0 difference in GPA)
    - Asymmetric Skill Swap:
        +15 pts if candidate's teach_subject matches user's need_subject
        +15 pts if user's teach_subject matches candidate's need_subject
    Returns:
        total_score (float, 0-100)
        breakdown (dict)
        tags (list of dicts with label, type, and pts)
    """
    total_score = 0.0
    tags = []
    
    # 1. Schedule Match (+40 pts if time_pref matches exactly)
    user_time = (user_profile.get("time_pref") or user_profile.get("study_hours") or "").strip().lower()
    cand_time = (candidate.get("time_pref") or candidate.get("study_hours") or "").strip().lower()
    
    user_is_night = "night" in user_time
    cand_is_night = "night" in cand_time

    schedule_pts = 0.0
    if user_is_night == cand_is_night and user_time != "":
        schedule_pts = 40.0
        icon = "🌙" if user_is_night else "🌅"
        label_time = "Night Owls" if user_is_night else "Early Birds"
        tags.append({
            "type": "schedule",
            "label": f"{icon} Peak Hours Sync: Both {label_time}",
            "pts": 40
        })
    else:
        label_u = "Night" if user_is_night else "Morning"
        label_c = "Night" if cand_is_night else "Morning"
        tags.append({
            "type": "schedule-mismatch",
            "label": f"⏰ Schedule Shift ({label_u} vs {label_c})",
            "pts": 0
        })
    total_score += schedule_pts

    # 2. Target GPA Alignment (Max +30 pts, 10 pts penalty per 1.0 diff)
    try:
        user_gpa = float(user_profile.get("target_gpa") or user_profile.get("target_cgpa") or 8.0)
        cand_gpa = float(candidate.get("target_gpa") or candidate.get("target_cgpa") or 8.0)
        diff = abs(user_gpa - cand_gpa)
        # Closer targets = higher score (30 - 10.0 * diff, min 0)
        gpa_pts = max(0.0, round(30.0 - (10.0 * diff), 1))
    except (ValueError, TypeError):
        diff = 0.0
        gpa_pts = 25.0

    total_score += gpa_pts
    tags.append({
        "type": "cgpa",
        "label": f"🎯 Target GPA Sync: {user_gpa:.1f} ↔ {cand_gpa:.1f} (Δ {diff:.1f})",
        "pts": gpa_pts
    })

    # 3. Asymmetric Skill Swap (Max +30 pts: +15 each direction)
    user_teach = (user_profile.get("teach_subject") or user_profile.get("strong_subject") or "").strip().lower()
    user_need = (user_profile.get("need_subject") or user_profile.get("weak_subject") or "").strip().lower()
    cand_teach = (candidate.get("teach_subject") or candidate.get("strong_subject") or "").strip().lower()
    cand_need = (candidate.get("need_subject") or candidate.get("weak_subject") or "").strip().lower()
    
    cand_teaches_user = (cand_teach == user_need and cand_teach != "")
    user_teaches_cand = (user_teach == cand_need and user_teach != "")
    
    skill_pts = 0.0
    cand_teach_display = candidate.get("teach_subject") or candidate.get("strong_subject")
    cand_need_display = candidate.get("need_subject") or candidate.get("weak_subject")

    if cand_teaches_user and user_teaches_cand:
        skill_pts = 30.0
        tags.append({
            "type": "skill-swap-perfect",
            "label": f"✨ Mutual Skill Swap: {cand_teach_display} 🔄 {cand_need_display}",
            "pts": 30
        })
    else:
        if cand_teaches_user:
            skill_pts += 15.0
            tags.append({
                "type": "skill-swap",
                "label": f"💡 Mentors You in: {cand_teach_display}",
                "pts": 15
            })
        if user_teaches_cand:
            skill_pts += 15.0
            tags.append({
                "type": "skill-swap",
                "label": f"🎓 You Mentor Them in: {cand_need_display}",
                "pts": 15
            })
        if not cand_teaches_user and not user_teaches_cand:
            tags.append({
                "type": "skill-neutral",
                "label": f"📚 Parallel Focus: {cand_teach_display}",
                "pts": 0
            })

    total_score += skill_pts

    # Round final score
    final_score = min(100.0, round(total_score, 1))

    # Add College Badge
    if candidate.get("college"):
        tags.insert(0, {
            "type": "college",
            "label": f"🏛️ {candidate['college']}",
            "pts": 0
        })

    breakdown = {
        "schedule_pts": schedule_pts,
        "cgpa_pts": gpa_pts,
        "skill_pts": skill_pts,
        "total_score": final_score
    }

    return final_score, breakdown, tags

# Alias for backward compatibility
calculate_match_score = calculate_compatibility

def assign_pod_roles(squad_members):
    """
    Assigns each squad member a distinct role from:
    ["concept_lead", "scribe", "time_tracker", "resource_lead"].
    Honors stated preferences first; conflicts / no_preference are resolved round-robin.
    """
    ALL_ROLES = ["concept_lead", "scribe", "time_tracker", "resource_lead"]
    available_roles = list(ALL_ROLES)
    assigned = {}

    # Pass 1: Stated preferences (first come / priority)
    for idx, member in enumerate(squad_members):
        pref = (member.get("role_preference") or "no_preference").strip().lower()
        if pref in available_roles:
            assigned[idx] = pref
            available_roles.remove(pref)

    # Pass 2: Round-robin assignment for remaining unassigned members
    for idx, member in enumerate(squad_members):
        if idx not in assigned:
            if available_roles:
                assigned[idx] = available_roles.pop(0)
            else:
                assigned[idx] = "resource_lead"

    for idx, member in enumerate(squad_members):
        member["assigned_role"] = assigned.get(idx, "concept_lead")

    return squad_members

def find_squad(user_profile, sprint_type="48hr_exam_prep"):
    """
    Forms a complementary 4-person study squad (User + Top 3 Peers) with:
    - College scoping (same university required)
    - Track pre-filtering (honor_roll requiring target_gpa >= 8.5 vs exchange)
    - Group cohesion pod-so-far greedy mutual compatibility evaluation
    - Distinct pod role assignment (concept_lead, scribe, time_tracker, resource_lead)
    - Secondary sort keys (matching_priority, reliability_score)
    """
    conn = get_db()
    cursor = conn.cursor()
    
    user_college = user_profile.get("college", "").strip()
    user_name = user_profile.get("name", "").strip()
    user_id = user_profile.get("id", 0)

    if user_college:
        cursor.execute("""
            SELECT * FROM students 
            WHERE LOWER(college) = LOWER(?) 
              AND id != ? 
              AND LOWER(name) != LOWER(?)
        """, (user_college, user_id, user_name))
    else:
        cursor.execute("""
            SELECT * FROM students 
            WHERE id != ? 
              AND LOWER(name) != LOWER(?)
        """, (user_id, user_name))
        
    rows = cursor.fetchall()
    conn.close()

    raw_candidates = [dict(r) for r in rows]

    # 1. Track Pre-Filtering
    user_track = (user_profile.get("track") or "exchange").strip().lower()
    if user_track not in ["exchange", "honor_roll"]:
        user_track = "exchange"

    eligible_candidates = []
    for cand in raw_candidates:
        c_track = (cand.get("track") or "exchange").strip().lower()
        try:
            c_gpa = float(cand.get("target_gpa") or cand.get("target_cgpa") or 0.0)
        except (ValueError, TypeError):
            c_gpa = 0.0

        if user_track == "honor_roll":
            # Honor roll only matches students with target_gpa >= 8.5 who also selected honor_roll
            if c_track == "honor_roll" and c_gpa >= 8.5:
                eligible_candidates.append(cand)
        else:
            # Exchange matches normally
            eligible_candidates.append(cand)

    # 2. Score individual match against user_profile
    for cand in eligible_candidates:
        score, breakdown, tags = calculate_match_score(user_profile, cand)
        cand["match_score"] = score
        cand["breakdown"] = breakdown
        cand["tags"] = tags
        cand["matching_priority"] = float(cand.get("matching_priority", 1.0))
        cand["reliability_score"] = float(cand.get("reliability_score", 95.0))

    # 3. Group Cohesion Pod-so-far Greedy Matching
    # Iteratively select peers that maximize mutual compatibility with the pod formed so far
    current_pod = [user_profile]
    remaining = list(eligible_candidates)
    top_3 = []

    while len(top_3) < 3 and remaining:
        best_cand = None
        best_eval = (-1.0, -1.0, -1.0)
        
        for cand in remaining:
            # Cohesion score: average compatibility with all current pod members
            compat_with_pod = [calculate_match_score(m, cand)[0] for m in current_pod]
            cohesion_score = sum(compat_with_pod) / len(compat_with_pod)
            
            # Secondary sort: matching_priority, reliability_score
            priority = cand.get("matching_priority", 1.0)
            reliability = cand.get("reliability_score", 95.0)
            
            eval_tuple = (cohesion_score, priority, reliability)
            if eval_tuple > best_eval:
                best_eval = eval_tuple
                best_cand = cand
                cand["cohesion_score"] = round(cohesion_score, 1)

        if best_cand:
            top_3.append(best_cand)
            current_pod.append(best_cand)
            remaining.remove(best_cand)

    # Sort all candidates by cohesion_score / match_score, matching_priority, reliability_score
    eligible_candidates.sort(
        key=lambda x: (x.get("cohesion_score", x.get("match_score", 0)), x.get("matching_priority", 1.0), x.get("reliability_score", 95.0)),
        reverse=True
    )

    # 4. Synergy & Group Cohesion Score Calculation
    synergy_score = round(sum(c["match_score"] for c in top_3) / len(top_3), 1) if top_3 else 0.0

    # Calculate overall squad cohesion across all pairwise members in final pod
    final_pod = [user_profile] + top_3
    pairwise_scores = []
    for i in range(len(final_pod)):
        for j in range(i + 1, len(final_pod)):
            p_score, _, _ = calculate_match_score(final_pod[i], final_pod[j])
            pairwise_scores.append(p_score)
    group_cohesion_score = round(sum(pairwise_scores) / len(pairwise_scores), 1) if pairwise_scores else synergy_score

    # 5. Pod Roles Assignment
    assign_pod_roles(final_pod)

    # Squad highlights
    squad_strengths = set()
    user_str = user_profile.get("teach_subject") or user_profile.get("strong_subject")
    if user_str:
        squad_strengths.add(user_str)
    for c in top_3:
        c_str = c.get("teach_subject") or c.get("strong_subject")
        if c_str:
            squad_strengths.add(c_str)

    # Generate stable squad_id
    import re
    safe_name = re.sub(r'[^a-zA-Z0-9]', '', user_name).lower() or "lead"
    safe_college = re.sub(r'[^a-zA-Z0-9]', '', user_college).lower() or "campus"
    peer_ids = "-".join(str(c.get("id", 0)) for c in top_3)
    squad_id = f"squad_{safe_college}_{safe_name}_{peer_ids}"

    return {
        "squad_id": squad_id,
        "user": user_profile,
        "college": user_college,
        "track": user_track,
        "sprint_type": sprint_type,
        "total_in_college": len(eligible_candidates),
        "top_candidates": top_3,
        "all_ranked": eligible_candidates,
        "synergy_score": synergy_score,
        "group_cohesion_score": group_cohesion_score,
        "squad_strengths": list(squad_strengths)
    }
