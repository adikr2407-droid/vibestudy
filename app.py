import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from database import init_db, get_db, add_student, COLLEGES, get_squad_messages, add_squad_message, init_squad_chat, save_squad_session, get_squad_session
from matching import find_squad, calculate_compatibility

app = Flask(__name__, static_folder="static", template_folder="templates")

ENGINEERING_SUBJECTS = [
    "Python",
    "Digital Logic",
    "Calculus",
    "Physics",
    "Data Structures",
    "Data Structures & Algorithms",
    "Operating Systems",
    "Machine Learning & AI",
    "Database Management Systems",
    "Computer Networks"
]

# Ensure DB is initialized
init_db()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

@app.route("/api/subjects", methods=["GET"])
def get_subjects():
    return jsonify({"subjects": ENGINEERING_SUBJECTS})

@app.route("/api/colleges", methods=["GET"])
def get_colleges():
    return jsonify({"colleges": COLLEGES})

@app.route("/api/candidates", methods=["GET"])
def get_candidates():
    college = request.args.get("college", "").strip()
    conn = get_db()
    cursor = conn.cursor()
    if college and college.lower() != "all":
        cursor.execute("SELECT * FROM students WHERE LOWER(college) = LOWER(?) ORDER BY id DESC", (college,))
    else:
        cursor.execute("SELECT * FROM students ORDER BY id DESC")
    rows = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return jsonify({"candidates": rows, "count": len(rows), "college": college or "All"})

@app.route("/api/students", methods=["POST"])
def create_student():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    college = (data.get("college") or "Bennett University").strip() or "Bennett University"
    section = data.get("section", "").strip()
    
    raw_time = str(data.get("time_pref") or data.get("study_hours") or "Night")
    time_pref = "Night" if "night" in raw_time.lower() else "Morning"
    study_hours = "Night Owl" if time_pref == "Night" else "Early Bird"

    try:
        target_gpa = float(data.get("target_gpa") or data.get("target_cgpa") or 8.0)
    except (ValueError, TypeError):
        target_gpa = 8.0
    target_cgpa = target_gpa

    teach_subject = (data.get("teach_subject") or data.get("strong_subject") or "").strip()
    need_subject = (data.get("need_subject") or data.get("weak_subject") or "").strip()
    strong_subject = teach_subject
    weak_subject = need_subject
    bio = data.get("bio", "Engineering undergraduate student ready for study sprints.").strip()

    track = (data.get("track") or "exchange").strip().lower()
    role_preference = (data.get("role_preference") or "no_preference").strip().lower()

    if not name or not section:
        return jsonify({"error": "Name and Section are required."}), 400

    if not strong_subject or not weak_subject:
        return jsonify({"error": "Both strong and weak subjects are required."}), 400

    if strong_subject.lower() == weak_subject.lower():
        return jsonify({"error": "Strong and weak subjects cannot be the same."}), 400

    new_student = add_student({
        "name": name,
        "college": college,
        "section": section,
        "time_pref": time_pref,
        "study_hours": study_hours,
        "target_gpa": target_gpa,
        "target_cgpa": target_cgpa,
        "teach_subject": teach_subject,
        "strong_subject": strong_subject,
        "need_subject": need_subject,
        "weak_subject": weak_subject,
        "reputation_score": 95,
        "reliability_score": 95.0,
        "review_count": 1,
        "bio": bio,
        "track": track,
        "role_preference": role_preference,
        "study_credits": int(data.get("study_credits", 50)),
        "matching_priority": float(data.get("matching_priority", 1.0))
    })

    return jsonify({
        "status": "success",
        "message": f"Profile for {name} ({college}) saved to candidate pool!",
        "student": new_student
    }), 201

@app.route("/api/match", methods=["POST"])
def match_squad():
    data = request.get_json() or {}
    
    # Basic validation
    name = data.get("name", "").strip()
    if not name:
        name = "Learner"

    college = (data.get("college") or "Bennett University").strip() or "Bennett University"
    section = data.get("section", "CSE-A").strip()
    
    raw_time = str(data.get("time_pref") or data.get("study_hours") or "Night")
    time_pref = "Night" if "night" in raw_time.lower() else "Morning"
    study_hours = "Night Owl" if time_pref == "Night" else "Early Bird"

    try:
        target_gpa = float(data.get("target_gpa") or data.get("target_cgpa") or 8.5)
    except (ValueError, TypeError):
        target_gpa = 8.5
    target_cgpa = target_gpa

    teach_subject = (data.get("teach_subject") or data.get("strong_subject") or "").strip()
    need_subject = (data.get("need_subject") or data.get("weak_subject") or "").strip()
    strong_subject = teach_subject
    weak_subject = need_subject

    save_to_pool = bool(data.get("save_to_pool", False))
    bio = data.get("bio", "Engineering undergraduate student ready for study sprints.").strip()
    track = (data.get("track") or "exchange").strip().lower()
    role_preference = (data.get("role_preference") or "no_preference").strip().lower()
    sprint_type = (data.get("sprint_type") or "48hr_exam_prep").strip().lower()

    if not strong_subject or not weak_subject:
        return jsonify({"error": "Please provide both strong and weak subjects."}), 400

    if strong_subject.lower() == weak_subject.lower():
        return jsonify({"error": "Strong and weak subjects cannot be the same."}), 400

    user_id = 0
    if save_to_pool:
        saved_student = add_student({
            "name": name,
            "college": college,
            "section": section,
            "time_pref": time_pref,
            "study_hours": study_hours,
            "target_gpa": target_gpa,
            "target_cgpa": target_cgpa,
            "teach_subject": teach_subject,
            "strong_subject": strong_subject,
            "need_subject": need_subject,
            "weak_subject": weak_subject,
            "reputation_score": 100,
            "reliability_score": 100.0,
            "review_count": 1,
            "bio": bio,
            "track": track,
            "role_preference": role_preference,
            "study_credits": 50,
            "matching_priority": 1.0,
            "sessions_taught": 0,
            "is_mentor": 0
        })
        user_id = saved_student["id"]

    user_profile = {
        "id": user_id,
        "name": name,
        "college": college,
        "section": section,
        "avatar": f"https://api.dicebear.com/7.x/bottts/svg?seed={name}&backgroundColor=ffd5dc",
        "time_pref": time_pref,
        "study_hours": study_hours,
        "target_gpa": target_gpa,
        "target_cgpa": target_cgpa,
        "teach_subject": teach_subject,
        "strong_subject": strong_subject,
        "need_subject": need_subject,
        "weak_subject": weak_subject,
        "reputation_score": 100,
        "reliability_score": 100.0,
        "track": track,
        "role_preference": role_preference,
        "is_user": True,
        "saved_to_pool": save_to_pool,
        "sessions_taught": 0,
        "is_mentor": 0,
        "verified_mentor": 0,
        "teaching_sessions_completed": 0
    }

    squad_result = find_squad(user_profile, sprint_type=sprint_type)
    session_record = save_squad_session(squad_result["squad_id"], college, sprint_type=sprint_type)
    squad_result["session"] = session_record
    
    initial_messages = init_squad_chat(squad_result["squad_id"], user_profile, squad_result["top_candidates"])
    return jsonify({
        "status": "success",
        "squad": squad_result,
        "saved_to_pool": save_to_pool,
        "initial_messages": initial_messages
    })

@app.route("/api/review", methods=["POST"])
def submit_review():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    reviewer_name = data.get("reviewer_name", "Squad Lead").strip()
    punctual = 1 if data.get("punctual", True) else 0
    focused = 1 if data.get("focused", True) else 0
    try:
        rating = int(data.get("rating", 5))
        rating = max(1, min(5, rating))
    except (ValueError, TypeError):
        rating = 5

    if not student_id:
        return jsonify({"error": "Student ID is required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        return jsonify({"error": "Student not found."}), 404

    # Calculate session score:
    # punctual: 40 pts, focused: 40 pts, rating: up to 20 pts (4 pts per star)
    session_score = (40.0 if punctual else 15.0) + (40.0 if focused else 15.0) + (rating * 4.0)

    old_score = student["reliability_score"]
    old_count = student["review_count"]
    new_count = old_count + 1
    new_score = round(((old_score * old_count) + session_score) / new_count, 1)
    new_score = min(100.0, max(0.0, new_score))

    cursor.execute("""
        INSERT INTO peer_reviews (student_id, reviewer_name, punctual, focused, rating)
        VALUES (?, ?, ?, ?, ?)
    """, (student_id, reviewer_name, punctual, focused, rating))

    # Check mentor teaching session qualification
    old_teaching = student["sessions_taught"] if "sessions_taught" in student.keys() else (student["teaching_sessions_completed"] if "teaching_sessions_completed" in student.keys() else 0)
    old_mentor = student["is_mentor"] if "is_mentor" in student.keys() else (student["verified_mentor"] if "verified_mentor" in student.keys() else 0)

    if punctual and focused and rating >= 4:
        new_teaching = (old_teaching or 0) + 1
        new_mentor = 1 if new_teaching >= 15 else (old_mentor or 0)
    else:
        new_teaching = old_teaching or 0
        new_mentor = old_mentor or 0

    cursor.execute("""
        UPDATE students
        SET reliability_score = ?, reputation_score = ?, review_count = ?,
            teaching_sessions_completed = ?, verified_mentor = ?,
            sessions_taught = ?, is_mentor = ?
        WHERE id = ?
    """, (new_score, int(new_score), new_count, new_teaching, new_mentor, new_teaching, new_mentor, student_id))
    
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": f"Peer review logged for {student['name']}",
        "student_id": student_id,
        "old_score": old_score,
        "new_score": new_score,
        "review_count": new_count,
        "teaching_sessions_completed": new_teaching,
        "verified_mentor": new_mentor,
        "sessions_taught": new_teaching,
        "is_mentor": new_mentor
    })

@app.route("/api/session/checkin", methods=["POST"])
def session_checkin():
    data = request.get_json() or {}
    student_id = data.get("student_id")
    action = (data.get("action") or "").strip().lower()
    squad_id = data.get("squad_id", "")

    if not student_id or action not in ["start", "complete", "noshow"]:
        return jsonify({"error": "Valid student_id and action ('start', 'complete', 'noshow') are required."}), 400

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student = cursor.fetchone()

    if not student:
        conn.close()
        return jsonify({"error": "Student not found."}), 404

    current_credits = student["study_credits"] if "study_credits" in student.keys() else 50
    priority = student["matching_priority"] if "matching_priority" in student.keys() else 1.0
    review_count = student["review_count"] if "review_count" in student.keys() else 1

    DEPOSIT = 10
    BONUS = 5

    if action == "start":
        if current_credits < DEPOSIT:
            conn.close()
            return jsonify({
                "status": "error",
                "error": f"Insufficient study credits. Need {DEPOSIT} credits to lock sprint deposit, but currently have {current_credits}."
            }), 400
        new_credits = current_credits - DEPOSIT
        cursor.execute("UPDATE students SET study_credits = ? WHERE id = ?", (new_credits, student_id))
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success",
            "action": "start",
            "deposit_locked": DEPOSIT,
            "study_credits": new_credits,
            "matching_priority": priority,
            "message": f"Deposit of {DEPOSIT} credits locked for sprint. Remaining balance: {new_credits} credits."
        })

    elif action == "complete":
        refund_and_bonus = DEPOSIT + BONUS
        new_credits = current_credits + refund_and_bonus
        new_priority = round(min(1.5, priority + 0.05), 2)
        cursor.execute("UPDATE students SET study_credits = ?, matching_priority = ? WHERE id = ?", (new_credits, new_priority, student_id))
        conn.commit()
        conn.close()
        return jsonify({
            "status": "success",
            "action": "complete",
            "refunded": DEPOSIT,
            "bonus": BONUS,
            "net_gain": BONUS,
            "study_credits": new_credits,
            "matching_priority": new_priority,
            "message": f"Sprint completed on time! Refunded {DEPOSIT} deposit + {BONUS} bonus credits. New balance: {new_credits} credits."
        })

    elif action == "noshow":
        # First-time users (review_count == 0) get one grace session
        is_first_time = (review_count == 0)
        if is_first_time:
            new_credits = current_credits + DEPOSIT
            new_priority = priority
            cursor.execute("UPDATE students SET study_credits = ? WHERE id = ?", (new_credits, student_id))
            conn.commit()
            conn.close()
            return jsonify({
                "status": "success",
                "action": "noshow",
                "grace_session": True,
                "study_credits": new_credits,
                "matching_priority": new_priority,
                "message": "First-time user grace session applied: deposit restored with no credits forfeited."
            })
        else:
            new_priority = round(max(0.2, priority - 0.15), 2)
            cursor.execute("UPDATE students SET matching_priority = ? WHERE id = ?", (new_priority, student_id))
            conn.commit()
            conn.close()
            return jsonify({
                "status": "success",
                "action": "noshow",
                "grace_session": False,
                "deposit_forfeited": DEPOSIT,
                "study_credits": current_credits,
                "matching_priority": new_priority,
                "message": f"Unexcused no-show: {DEPOSIT} credit deposit forfeited. Matching priority reduced to {new_priority}."
            })

@app.route("/api/squad/<squad_id>", methods=["GET"])
def get_squad_info(squad_id):
    session_info = get_squad_session(squad_id)
    if not session_info:
        return jsonify({"status": "not_found", "squad_id": squad_id, "is_expired": False}), 404
    return jsonify({
        "status": "success",
        "session": session_info,
        "session_status": session_info.get("status"),
        "expired": session_info.get("expired", False),
        "sprint_type": session_info.get("sprint_type"),
        "expires_at": session_info.get("expires_at"),
        "time_remaining": session_info.get("time_remaining")
    })

@app.route("/api/squad/<squad_id>/messages", methods=["GET"])
def get_messages_route(squad_id):
    channel = request.args.get("channel")
    messages = get_squad_messages(squad_id, channel=channel)
    return jsonify({"status": "success", "squad_id": squad_id, "messages": messages, "count": len(messages)})

@app.route("/api/squad/<squad_id>/messages", methods=["POST"])
def post_message_route(squad_id):
    data = request.get_json() or {}
    channel = data.get("channel", "lounge").strip() or "lounge"
    sender_name = data.get("sender_name", "Squad Lead").strip()
    sender_avatar = data.get("sender_avatar", "").strip() or f"https://api.dicebear.com/7.x/bottts/svg?seed={sender_name}&backgroundColor=ffd5dc"
    sender_role = data.get("sender_role", "Squad Lead").strip()
    sender_id = int(data.get("sender_id", 0))
    message = data.get("message", "").strip()

    if not message:
        return jsonify({"error": "Message content cannot be empty."}), 400

    new_msg = add_squad_message(
        squad_id=squad_id,
        channel=channel,
        sender_name=sender_name,
        sender_avatar=sender_avatar,
        sender_role=sender_role,
        message=message,
        sender_id=sender_id
    )

    return jsonify({"status": "success", "message": new_msg}), 201

@app.route("/api/squad/<squad_id>/simulate_reply", methods=["POST"])
def simulate_peer_reply_route(squad_id):
    data = request.get_json() or {}
    channel = data.get("channel", "lounge").strip() or "lounge"
    user_text = data.get("user_message", "").lower()
    peer_name = data.get("peer_name")
    peer_avatar = data.get("peer_avatar")
    peer_strong = data.get("peer_strong", "Core Subjects")
    peer_id = int(data.get("peer_id", 0))

    if any(w in user_text for w in ["meet", "when", "time", "schedule", "call", "zoom"]):
        reply_text = "I'm free after 8:30 PM tonight! Let's meet at the library 2nd floor or start a study huddle."
    elif any(w in user_text for w in ["note", "notes", "material", "slides", "pdf"]):
        reply_text = f"Sure! I have compiled quick cheat-sheets and past paper solutions for {peer_strong}."
    elif any(w in user_text for w in ["pomo", "timer", "sprint", "start", "focus", "deep"]):
        reply_text = "Let's do this! Starting the 50-minute Pomodoro focus sprint now. Phones on silent!"
    elif any(w in user_text for w in ["break", "coffee", "tea", "tired", "pause"]):
        reply_text = "Great sprint everyone! Let's take a 10-minute break and recharge."
    elif any(w in user_text for w in ["exam", "final", "quiz", "test", "cgpa", "grade"]):
        reply_text = "If we keep up this momentum, a 9.0+ semester CGPA is definitely within reach! 🚀"
    else:
        replies = [
            f"Sounds great! Looking forward to mastering {peer_strong} together.",
            "Count me in! Let me know which problem set we're tackling first.",
            "Awesome, thanks for setting this up! Ready whenever the squad is.",
            "Got it! I will review the lecture slides before our next sprint."
        ]
        import random
        reply_text = random.choice(replies)

    if not peer_name:
        peer_name = "Study Peer"
    if not peer_avatar:
        peer_avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={peer_name}&backgroundColor=b6e3f4"

    new_msg = add_squad_message(
        squad_id=squad_id,
        channel=channel,
        sender_name=peer_name,
        sender_avatar=peer_avatar,
        sender_role="Peer",
        message=reply_text,
        sender_id=peer_id
    )

    return jsonify({"status": "success", "message": new_msg})

@app.route("/api/reset", methods=["POST"])
def reset_database():
    init_db(force_reset=True)
    return jsonify({"status": "success", "message": "Database reset to initial 6 candidates."})

@app.route("/certificate/<int:student_id>")
def view_certificate(student_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    student_row = cursor.fetchone()
    conn.close()

    if not student_row:
        return render_template(
            "certificate_denied.html",
            student=None,
            sessions_taught=0,
            needed_sessions=15,
            remaining_sessions=15,
            error_title="Student Profile Not Found",
            error_message=f"No student record found in database with ID #{student_id}."
        ), 404

    student = dict(student_row)
    sessions_taught = student.get("sessions_taught")
    if sessions_taught is None:
        sessions_taught = student.get("teaching_sessions_completed", 0)
    sessions_taught = int(sessions_taught or 0)

    raw_mentor = student.get("is_mentor")
    if raw_mentor is None:
        raw_mentor = student.get("verified_mentor", 0)
    is_mentor = int(raw_mentor or 0) == 1

    is_qualified = is_mentor or (sessions_taught >= 15)
    if not is_qualified:
        return render_template(
            "certificate_denied.html",
            student=student,
            sessions_taught=sessions_taught,
            needed_sessions=15,
            remaining_sessions=max(0, 15 - sessions_taught),
            error_title="Mentor Certification Pending",
            error_message=f"{student['name']} has completed {sessions_taught} out of 15 required high-rated peer teaching sprints to achieve Verified Peer Mentor status."
        ), 403

    import hashlib
    hash_suffix = hashlib.md5(f"vibestudy-cert-{student_id}-{student['name']}".encode()).hexdigest()[:4].upper()
    credential_id = f"VIBE-CERT-{student_id:04d}{hash_suffix}"
    
    import datetime
    issue_date = datetime.date.today().strftime("%B %d, %Y")
    primary_subject = student.get("teach_subject") or student.get("strong_subject") or "Engineering Fundamentals"

    return render_template(
        "certificate.html",
        student=student,
        credential_id=credential_id,
        issue_date=issue_date,
        primary_subject=primary_subject,
        sessions_taught=sessions_taught
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
