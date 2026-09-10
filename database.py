import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "vibestudy.db")

COLLEGES = [
    "Bennett University",
    "Apex Institute of Technology",
    "Metro Tech University",
    "Imperial Institute of Computing",
    "National Engineering College"
]

SEEDED_STUDENTS = [
    # --- Bennett University ---
    {
        "name": "Ishaan Malhotra",
        "college": "Bennett University",
        "section": "CSE-AI",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Ishaan&backgroundColor=b6e3f4",
        "time_pref": "Night",
        "study_hours": "Night Owl",
        "target_gpa": 8.8,
        "target_cgpa": 8.8,
        "teach_subject": "Python",
        "strong_subject": "Python",
        "need_subject": "Data Structures",
        "weak_subject": "Data Structures",
        "reputation_score": 96,
        "reliability_score": 96.0,
        "review_count": 8,
        "track": "honor_roll",
        "role_preference": "concept_lead",
        "study_credits": 60,
        "matching_priority": 1.1,
        "teaching_sessions_completed": 8,
        "sessions_taught": 8,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Bennett University CSE-AI sophomore grinding PyTorch & neural architectures."
    },
    {
        "name": "Diya Kashyap",
        "college": "Bennett University",
        "section": "CSE-A",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Diya&backgroundColor=ffd5dc",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 9.2,
        "target_cgpa": 9.2,
        "teach_subject": "Data Structures",
        "strong_subject": "Data Structures",
        "need_subject": "Digital Logic",
        "weak_subject": "Digital Logic",
        "reputation_score": 98,
        "reliability_score": 98.0,
        "review_count": 11,
        "track": "honor_roll",
        "role_preference": "scribe",
        "study_credits": 75,
        "matching_priority": 1.2,
        "teaching_sessions_completed": 16,
        "sessions_taught": 16,
        "verified_mentor": 1,
        "is_mentor": 1,
        "bio": "Bennett ACM chapter member & DSA enthusiast. Loves morning high-focus sprints."
    },
    {
        "name": "Aryan Singhal",
        "college": "Bennett University",
        "section": "ECE-A",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Aryan&backgroundColor=d1d4f9",
        "time_pref": "Night",
        "study_hours": "Night Owl",
        "target_gpa": 8.4,
        "target_cgpa": 8.4,
        "teach_subject": "Digital Logic",
        "strong_subject": "Digital Logic",
        "need_subject": "Data Structures",
        "weak_subject": "Data Structures",
        "reputation_score": 93,
        "reliability_score": 93.0,
        "review_count": 7,
        "track": "exchange",
        "role_preference": "time_tracker",
        "study_credits": 50,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 4,
        "sessions_taught": 4,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Bennett Robotics club lead. Hardware & logic circuits whiz seeking DSA support."
    },
    {
        "name": "Riddhi Aggarwal",
        "college": "Bennett University",
        "section": "CSE-B",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Riddhi&backgroundColor=c0aede",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 8.7,
        "target_cgpa": 8.7,
        "teach_subject": "Calculus",
        "strong_subject": "Calculus",
        "need_subject": "Physics",
        "weak_subject": "Physics",
        "reputation_score": 94,
        "reliability_score": 94.0,
        "review_count": 9,
        "track": "honor_roll",
        "role_preference": "no_preference",
        "study_credits": 55,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 6,
        "sessions_taught": 6,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Full-stack developer at Bennett looking for math study partners for semester projects."
    },
    {
        "name": "Kunal Batra",
        "college": "Bennett University",
        "section": "CSE-C",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Kunal&backgroundColor=ffdfbf",
        "time_pref": "Night",
        "study_hours": "Night Owl",
        "target_gpa": 8.1,
        "target_cgpa": 8.1,
        "teach_subject": "Physics",
        "strong_subject": "Physics",
        "need_subject": "Calculus",
        "weak_subject": "Calculus",
        "reputation_score": 90,
        "reliability_score": 90.0,
        "review_count": 5,
        "track": "exchange",
        "role_preference": "concept_lead",
        "study_credits": 50,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 3,
        "sessions_taught": 3,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Linux kernel tinkerer & physics whiz from Bennett University."
    },

    # --- Apex Institute of Technology ---
    {
        "name": "Rohan Sharma",
        "college": "Apex Institute of Technology",
        "section": "CSE-A",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Rohan&backgroundColor=b6e3f4",
        "time_pref": "Night",
        "study_hours": "Night Owl",
        "target_gpa": 8.8,
        "target_cgpa": 8.8,
        "teach_subject": "Data Structures",
        "strong_subject": "Data Structures",
        "need_subject": "Digital Logic",
        "weak_subject": "Digital Logic",
        "reputation_score": 95,
        "reliability_score": 95.0,
        "review_count": 8,
        "track": "honor_roll",
        "role_preference": "concept_lead",
        "study_credits": 60,
        "matching_priority": 1.1,
        "teaching_sessions_completed": 10,
        "sessions_taught": 10,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Competitive programmer & LeetCode grinder. Loves late night coding sessions."
    },
    {
        "name": "Kabir Mehta",
        "college": "Apex Institute of Technology",
        "section": "CSE-A",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Kabir&backgroundColor=d1d4f9",
        "time_pref": "Night",
        "study_hours": "Night Owl",
        "target_gpa": 7.6,
        "target_cgpa": 7.6,
        "teach_subject": "Python",
        "strong_subject": "Python",
        "need_subject": "Data Structures",
        "weak_subject": "Data Structures",
        "reputation_score": 88,
        "reliability_score": 88.0,
        "review_count": 5,
        "track": "exchange",
        "role_preference": "scribe",
        "study_credits": 50,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 2,
        "sessions_taught": 2,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Full-stack project builder. Needs help mastering recursion and graph algorithms."
    },
    {
        "name": "Devansh Verma",
        "college": "Apex Institute of Technology",
        "section": "CSE-B",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Devansh&backgroundColor=ffdfbf",
        "time_pref": "Night",
        "study_hours": "Night Owl",
        "target_gpa": 8.1,
        "target_cgpa": 8.1,
        "teach_subject": "Physics",
        "strong_subject": "Physics",
        "need_subject": "Calculus",
        "weak_subject": "Calculus",
        "reputation_score": 90,
        "reliability_score": 90.0,
        "review_count": 9,
        "track": "exchange",
        "role_preference": "time_tracker",
        "study_credits": 50,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 4,
        "sessions_taught": 4,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Systems programmer who enjoys threading and memory management deep dives."
    },
    {
        "name": "Sneha Roy",
        "college": "Apex Institute of Technology",
        "section": "CSE-C",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Sneha&backgroundColor=b6e3f4",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 8.9,
        "target_cgpa": 8.9,
        "teach_subject": "Calculus",
        "strong_subject": "Calculus",
        "need_subject": "Physics",
        "weak_subject": "Physics",
        "reputation_score": 94,
        "reliability_score": 94.0,
        "review_count": 10,
        "track": "honor_roll",
        "role_preference": "no_preference",
        "study_credits": 65,
        "matching_priority": 1.1,
        "teaching_sessions_completed": 15,
        "sessions_taught": 15,
        "verified_mentor": 1,
        "is_mentor": 1,
        "bio": "Calculus & linear algebra enthusiast preparing for semester finals."
    },

    # --- Metro Tech University ---
    {
        "name": "Ananya Iyer",
        "college": "Metro Tech University",
        "section": "CSE-B",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Ananya&backgroundColor=ffd5dc",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 9.2,
        "target_cgpa": 9.2,
        "teach_subject": "Calculus",
        "strong_subject": "Calculus",
        "need_subject": "Python",
        "weak_subject": "Python",
        "reputation_score": 98,
        "reliability_score": 98.0,
        "review_count": 12,
        "track": "honor_roll",
        "role_preference": "concept_lead",
        "study_credits": 70,
        "matching_priority": 1.15,
        "teaching_sessions_completed": 12,
        "sessions_taught": 12,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Math nerd focused on calculus proofs and morning high-focus sprints."
    },
    {
        "name": "Priya Patel",
        "college": "Metro Tech University",
        "section": "ECE-A",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Priya&backgroundColor=c0aede",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 8.4,
        "target_cgpa": 8.4,
        "teach_subject": "Digital Logic",
        "strong_subject": "Digital Logic",
        "need_subject": "Calculus",
        "weak_subject": "Calculus",
        "reputation_score": 92,
        "reliability_score": 92.0,
        "review_count": 7,
        "track": "exchange",
        "role_preference": "scribe",
        "study_credits": 50,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 5,
        "sessions_taught": 5,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Logic gates & hardware lover. Looking for a study buddy to conquer calculus."
    },
    {
        "name": "Aarav Gupta",
        "college": "Metro Tech University",
        "section": "CSE-C",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Aarav&backgroundColor=d1d4f9",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 9.4,
        "target_cgpa": 9.4,
        "teach_subject": "Python",
        "strong_subject": "Python",
        "need_subject": "Physics",
        "weak_subject": "Physics",
        "reputation_score": 96,
        "reliability_score": 96.0,
        "review_count": 6,
        "track": "honor_roll",
        "role_preference": "time_tracker",
        "study_credits": 55,
        "matching_priority": 1.05,
        "teaching_sessions_completed": 7,
        "sessions_taught": 7,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Neural networks and Python enthusiast."
    },
    {
        "name": "Tanvi Joshi",
        "college": "Metro Tech University",
        "section": "CSE-B",
        "avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Tanvi&backgroundColor=ffd5dc",
        "time_pref": "Morning",
        "study_hours": "Early Bird",
        "target_gpa": 8.7,
        "target_cgpa": 8.7,
        "teach_subject": "Physics",
        "strong_subject": "Physics",
        "need_subject": "Digital Logic",
        "weak_subject": "Digital Logic",
        "reputation_score": 91,
        "reliability_score": 91.0,
        "review_count": 4,
        "track": "honor_roll",
        "role_preference": "no_preference",
        "study_credits": 50,
        "matching_priority": 1.0,
        "teaching_sessions_completed": 3,
        "sessions_taught": 3,
        "verified_mentor": 0,
        "is_mentor": 0,
        "bio": "Linux kernel tinkerer and physics enthusiast."
    }
]

from datetime import datetime, timedelta, timezone

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reset=False, seed_demo=False):
    conn = get_db()
    cursor = conn.cursor()
    
    if force_reset:
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS peer_reviews")
        cursor.execute("DROP TABLE IF EXISTS squad_messages")
        cursor.execute("DROP TABLE IF EXISTS squad_sessions")
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            college TEXT NOT NULL DEFAULT 'Bennett University',
            section TEXT NOT NULL,
            avatar TEXT NOT NULL,
            time_pref TEXT NOT NULL,
            study_hours TEXT NOT NULL,
            target_gpa REAL NOT NULL,
            target_cgpa REAL NOT NULL,
            teach_subject TEXT NOT NULL,
            strong_subject TEXT NOT NULL,
            need_subject TEXT NOT NULL,
            weak_subject TEXT NOT NULL,
            reputation_score INTEGER DEFAULT 95,
            reliability_score REAL NOT NULL,
            review_count INTEGER DEFAULT 1,
            bio TEXT,
            track TEXT NOT NULL DEFAULT 'exchange',
            role_preference TEXT NOT NULL DEFAULT 'no_preference',
            study_credits INTEGER NOT NULL DEFAULT 50,
            matching_priority REAL NOT NULL DEFAULT 1.0,
            teaching_sessions_completed INTEGER NOT NULL DEFAULT 0,
            verified_mentor INTEGER NOT NULL DEFAULT 0,
            sessions_taught INTEGER NOT NULL DEFAULT 0,
            is_mentor INTEGER NOT NULL DEFAULT 0
        )
    """)

    # Non-destructive migration for existing tables
    cursor.execute("PRAGMA table_info(students)")
    existing_cols = {row["name"] for row in cursor.fetchall()}
    col_migrations = [
        ("track", "TEXT NOT NULL DEFAULT 'exchange'"),
        ("role_preference", "TEXT NOT NULL DEFAULT 'no_preference'"),
        ("study_credits", "INTEGER NOT NULL DEFAULT 50"),
        ("matching_priority", "REAL NOT NULL DEFAULT 1.0"),
        ("teaching_sessions_completed", "INTEGER NOT NULL DEFAULT 0"),
        ("verified_mentor", "INTEGER NOT NULL DEFAULT 0"),
        ("sessions_taught", "INTEGER NOT NULL DEFAULT 0"),
        ("is_mentor", "INTEGER NOT NULL DEFAULT 0")
    ]
    for col_name, col_type in col_migrations:
        if col_name not in existing_cols:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {col_name} {col_type}")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS peer_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            reviewer_name TEXT NOT NULL,
            punctual INTEGER NOT NULL,
            focused INTEGER NOT NULL,
            rating INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS squad_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            squad_id TEXT NOT NULL,
            channel TEXT NOT NULL DEFAULT 'lounge',
            sender_name TEXT NOT NULL,
            sender_avatar TEXT NOT NULL,
            sender_role TEXT DEFAULT 'Peer',
            sender_id INTEGER DEFAULT 0,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS squad_sessions (
            squad_id TEXT PRIMARY KEY,
            college TEXT NOT NULL,
            sprint_type TEXT NOT NULL DEFAULT '48hr_exam_prep',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP NOT NULL,
            status TEXT NOT NULL DEFAULT 'active'
        )
    """)
    
    cursor.execute("SELECT COUNT(*) as count FROM students")
    count = cursor.fetchone()["count"]
    conn.commit()
    conn.close()
    
    # Only seed if explicitly requested or environment variable SEED_DEMO_DATA=1
    auto_seed = seed_demo or (os.environ.get("SEED_DEMO_DATA", "").lower() in ("true", "1", "yes"))
    if auto_seed and count == 0:
        for s in SEEDED_STUDENTS:
            add_student(s)
        print("Database initialized and students seeded across colleges.")

def clear_all_students():
    """Wipes all registered student profiles, messages, and sessions for a completely clean live launch."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students")
    cursor.execute("DELETE FROM peer_reviews")
    cursor.execute("DELETE FROM squad_messages")
    cursor.execute("DELETE FROM squad_sessions")
    try:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('students', 'peer_reviews', 'squad_messages')")
    except Exception:
        pass
    conn.commit()
    conn.close()
    print("All student profiles cleared. Database is 100% clean.")

def seed_demo_students():
    """Populates the database with default multi-campus seed students."""
    for s in SEEDED_STUDENTS:
        add_student(s)
    print("Database seeded with sample campus student profiles.")

def add_student(data):
    """
    Inserts a new student into SQLite database, supporting both canonical and alias fields.
    """
    conn = get_db()
    cursor = conn.cursor()
    
    avatar = data.get("avatar")
    if not avatar:
        avatar = f"https://api.dicebear.com/7.x/bottts/svg?seed={data.get('name', 'Student')}&backgroundColor=b6e3f4"
        
    college = (data.get("college") or "Bennett University").strip() or "Bennett University"

    # Normalize time_pref & study_hours
    raw_time = str(data.get("time_pref") or data.get("study_hours") or "Night")
    time_pref = "Night" if "night" in raw_time.lower() else "Morning"
    study_hours = "Night Owl" if time_pref == "Night" else "Early Bird"

    # Normalize GPA
    try:
        target_gpa = float(data.get("target_gpa") or data.get("target_cgpa") or 8.0)
    except (ValueError, TypeError):
        target_gpa = 8.0
    target_cgpa = target_gpa

    # Normalize Teach / Need subjects
    teach_subject = (data.get("teach_subject") or data.get("strong_subject") or "Python").strip()
    strong_subject = teach_subject
    need_subject = (data.get("need_subject") or data.get("weak_subject") or "Data Structures").strip()
    weak_subject = need_subject

    # Normalize Reputation / Reliability
    try:
        reputation_score = int(float(data.get("reputation_score") or data.get("reliability_score") or 95))
    except (ValueError, TypeError):
        reputation_score = 95
    reliability_score = float(reputation_score)

    # Normalize Track
    track = (data.get("track") or "exchange").strip().lower()
    if track not in ["exchange", "honor_roll"]:
        track = "exchange"

    # Normalize Role Preference
    role_preference = (data.get("role_preference") or "no_preference").strip().lower()
    if role_preference not in ["concept_lead", "scribe", "time_tracker", "no_preference"]:
        role_preference = "no_preference"

    # Study credits & Matching priority
    try:
        study_credits = int(data.get("study_credits", 50))
    except (ValueError, TypeError):
        study_credits = 50

    try:
        matching_priority = float(data.get("matching_priority", 1.0))
    except (ValueError, TypeError):
        matching_priority = 1.0

    # Teaching sessions & verified mentor / sessions_taught & is_mentor
    try:
        raw_taught = data.get("sessions_taught") if data.get("sessions_taught") is not None else data.get("teaching_sessions_completed", 0)
        sessions_taught = int(raw_taught)
    except (ValueError, TypeError):
        sessions_taught = 0

    teaching_sessions_completed = sessions_taught

    raw_mentor = data.get("is_mentor") if data.get("is_mentor") is not None else data.get("verified_mentor", 0)
    is_explicit_mentor = int(raw_mentor or 0) == 1
    is_mentor = 1 if is_explicit_mentor or sessions_taught >= 15 else 0
    verified_mentor = is_mentor

    cursor.execute("""
        INSERT INTO students (
            name, college, section, avatar, 
            time_pref, study_hours, 
            target_gpa, target_cgpa, 
            teach_subject, strong_subject, 
            need_subject, weak_subject, 
            reputation_score, reliability_score, 
            review_count, bio,
            track, role_preference, study_credits,
            matching_priority, teaching_sessions_completed, verified_mentor,
            sessions_taught, is_mentor
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["name"],
        college,
        data.get("section", "Section A"),
        avatar,
        time_pref,
        study_hours,
        target_gpa,
        target_cgpa,
        teach_subject,
        strong_subject,
        need_subject,
        weak_subject,
        reputation_score,
        reliability_score,
        int(data.get("review_count", 1)),
        data.get("bio", "Engineering undergraduate student ready for study sprints."),
        track,
        role_preference,
        study_credits,
        matching_priority,
        teaching_sessions_completed,
        verified_mentor,
        sessions_taught,
        is_mentor
    ))
    new_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM students WHERE id = ?", (new_id,))
    new_student = dict(cursor.fetchone())
    conn.close()
    return new_student

def save_squad_session(squad_id, college, sprint_type="48hr_exam_prep", duration_hours=None):
    """
    Persists a squad micro-sprint session with computed expiration.
    """
    if not duration_hours:
        duration_hours = 48 if sprint_type == "48hr_exam_prep" else 168
    expires_at = datetime.now(timezone.utc) + timedelta(hours=duration_hours)
    expires_iso = expires_at.isoformat()
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO squad_sessions (squad_id, college, sprint_type, expires_at, status)
        VALUES (?, ?, ?, ?, 'active')
    """, (squad_id, college, sprint_type, expires_iso))
    conn.commit()
    conn.close()
    return {
        "squad_id": squad_id,
        "college": college,
        "sprint_type": sprint_type,
        "expires_at": expires_iso,
        "status": "active"
    }

def get_squad_session(squad_id):
    """
    Retrieves squad session and performs cron-free expiration check.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM squad_sessions WHERE squad_id = ?", (squad_id,))
    row = cursor.fetchone()
    if not row:
        conn.close()
        return None
    session_data = dict(row)
    expires_at_str = session_data.get("expires_at")
    is_expired = False
    remaining_seconds = 0
    if expires_at_str:
        try:
            expires_dt = datetime.fromisoformat(expires_at_str.replace("Z", "+00:00"))
            if expires_dt.tzinfo is None:
                expires_dt = expires_dt.replace(tzinfo=timezone.utc)
            now_dt = datetime.now(timezone.utc)
            diff = (expires_dt - now_dt).total_seconds()
            if diff <= 0:
                is_expired = True
                remaining_seconds = 0
                if session_data.get("status") == "active":
                    cursor.execute("UPDATE squad_sessions SET status = 'expired' WHERE squad_id = ?", (squad_id,))
                    conn.commit()
                    session_data["status"] = "expired"
            else:
                remaining_seconds = int(diff)
        except Exception:
            pass
    session_data["is_expired"] = is_expired
    session_data["remaining_seconds"] = remaining_seconds
    session_data["remaining_hours"] = round(remaining_seconds / 3600.0, 1)
    conn.close()
    return session_data

def get_squad_messages(squad_id, channel=None):
    """
    Retrieves messages for a squad, optionally filtered by channel.
    """
    conn = get_db()
    cursor = conn.cursor()
    if channel and channel.lower() != "all":
        cursor.execute("""
            SELECT * FROM squad_messages 
            WHERE squad_id = ? AND channel = ? 
            ORDER BY id ASC
        """, (squad_id, channel))
    else:
        cursor.execute("""
            SELECT * FROM squad_messages 
            WHERE squad_id = ? 
            ORDER BY id ASC
        """, (squad_id,))
    messages = [dict(r) for r in cursor.fetchall()]
    conn.close()
    return messages

def add_squad_message(squad_id, channel, sender_name, sender_avatar, sender_role, message, sender_id=0):
    """
    Adds a new message to the squad chat.
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO squad_messages (squad_id, channel, sender_name, sender_avatar, sender_role, sender_id, message)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (squad_id, channel, sender_name, sender_avatar, sender_role, sender_id, message))
    msg_id = cursor.lastrowid
    conn.commit()
    cursor.execute("SELECT * FROM squad_messages WHERE id = ?", (msg_id,))
    new_msg = dict(cursor.fetchone())
    conn.close()
    return new_msg

def init_squad_chat(squad_id, user_profile, peers):
    """
    Seeds initial greetings if squad_messages is empty for this squad.
    """
    existing = get_squad_messages(squad_id)
    if existing:
        return existing

    user_name = user_profile.get("name", "Lead")
    college = user_profile.get("college", "University")
    user_strong = user_profile.get("strong_subject", "Algorithms")

    # 1. System announcement
    add_squad_message(
        squad_id=squad_id,
        channel="lounge",
        sender_name="System",
        sender_avatar="https://api.dicebear.com/7.x/bottts/svg?seed=System&backgroundColor=6366f1",
        sender_role="System",
        message=f"🎉 Study Squad formed at {college}! 4 members connected and ready to collaborate.",
        sender_id=0
    )

    # 2. Peer 1 greeting
    if len(peers) > 0:
        p1 = peers[0]
        add_squad_message(
            squad_id=squad_id,
            channel="lounge",
            sender_name=p1["name"],
            sender_avatar=p1["avatar"],
            sender_role="Peer",
            sender_id=p1.get("id", 0),
            message=f"Hey {user_name}! Great synergy match! Saw you teach {user_strong}—definitely looking forward to our study sprints."
        )

    # 3. Peer 2 greeting
    if len(peers) > 1:
        p2 = peers[1]
        p2_strong = p2.get("strong_subject", "Core Engineering")
        add_squad_message(
            squad_id=squad_id,
            channel="lounge",
            sender_name=p2["name"],
            sender_avatar=p2["avatar"],
            sender_role="Peer",
            sender_id=p2.get("id", 0),
            message=f"Hey everyone! I can share notes on {p2_strong}. When are we kicking off our first Pomodoro sprint?"
        )

    return get_squad_messages(squad_id)

if __name__ == "__main__":
    init_db(force_reset=True)

