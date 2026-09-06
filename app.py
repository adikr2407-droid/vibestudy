import os
from flask import Flask, request, jsonify, render_template, send_from_directory
from database import init_db, get_db, add_student, COLLEGES, get_squad_messages, add_squad_message, init_squad_chat
from matching import find_squad, calculate_compatibility

app = Flask(__name__, static_folder="static", template_folder="templates")

ENGINEERING_SUBJECTS = [
    "Python",
    "Digital Logic",
    "Calculus",
    "Physics",
    "Data Structures",
    "Operating Systems",
    "Machine Learning & AI",
    "Database Management Systems"
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
        "bio": bio
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
            "bio": bio
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
        "is_user": True,
        "saved_to_pool": save_to_pool
    }

    squad_result = find_squad(user_profile)
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

    cursor.execute("""
        UPDATE students
        SET reliability_score = ?, reputation_score = ?, review_count = ?
        WHERE id = ?
    """, (new_score, int(new_score), new_count, student_id))
    
    conn.commit()
    conn.close()

    return jsonify({
        "status": "success",
        "message": f"Peer review logged for {student['name']}",
        "student_id": student_id,
        "old_score": old_score,
        "new_score": new_score,
        "review_count": new_count
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

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
