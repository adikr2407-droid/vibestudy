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

def find_squad(user_profile):
    """
    Ranks candidates against user_profile strictly from the same college
    and selects top 3 to form a 4-person squad (User + Top 3).
    Ensures user does not match with themselves.
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

    candidates_scored = []
    for r in rows:
        cand_dict = dict(r)
        score, breakdown, tags = calculate_match_score(user_profile, cand_dict)
        cand_dict["match_score"] = score
        cand_dict["breakdown"] = breakdown
        cand_dict["tags"] = tags
        candidates_scored.append(cand_dict)

    # Sort candidates by match_score descending, then reliability_score descending
    candidates_scored.sort(key=lambda x: (x["match_score"], x["reliability_score"]), reverse=True)

    # Top 3 candidates form the squad with user
    top_3 = candidates_scored[:3]
    synergy_score = round(sum(c["match_score"] for c in top_3) / len(top_3), 1) if top_3 else 0.0

    # Squad highlights
    squad_strengths = set()
    squad_strengths.add(user_profile.get("strong_subject"))
    for c in top_3:
        squad_strengths.add(c["strong_subject"])
    squad_strengths.discard(None)
    squad_strengths.discard("")

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
        "total_in_college": len(candidates_scored),
        "top_candidates": top_3,
        "all_ranked": candidates_scored,
        "synergy_score": synergy_score,
        "squad_strengths": list(squad_strengths)
    }
