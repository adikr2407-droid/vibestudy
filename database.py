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
        "bio": "Linux kernel tinkerer and physics enthusiast."
    }
]

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(force_reset=False):
    conn = get_db()
    cursor = conn.cursor()
    
    if force_reset:
        cursor.execute("DROP TABLE IF EXISTS students")
        cursor.execute("DROP TABLE IF EXISTS peer_reviews")
        cursor.execute("DROP TABLE IF EXISTS squad_messages")
    
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
            bio TEXT
        )
    """)

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
    
    cursor.execute("SELECT COUNT(*) as count FROM students")
    count = cursor.fetchone()["count"]
    conn.close()
    
    if count == 0:
        for s in SEEDED_STUDENTS:
            add_student(s)
        print("Database initialized and students seeded across colleges.")

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

    cursor.execute("""
        INSERT INTO students (
            name, college, section, avatar, 
            time_pref, study_hours, 
            target_gpa, target_cgpa, 
            teach_subject, strong_subject, 
            need_subject, weak_subject, 
            reputation_score, reliability_score, 
            review_count, bio
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
        data.get("bio", "Engineering undergraduate student ready for study sprints.")
    ))
    new_id = cursor.lastrowid
    conn.commit()
    
    cursor.execute("SELECT * FROM students WHERE id = ?", (new_id,))
    new_student = dict(cursor.fetchone())
    conn.close()
    return new_student

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

