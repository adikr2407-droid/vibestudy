import unittest
import json
import os
from database import init_db, get_db, add_student, clear_all_students
from matching import calculate_match_score, find_squad
from app import app

class TestVibeStudy(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        clear_all_students()

    def setUp(self):
        self.client = app.test_client()
        init_db(force_reset=True, seed_demo=True)

    def test_database_seeding(self):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as cnt FROM students")
        count = cursor.fetchone()["cnt"]
        conn.close()
        self.assertEqual(count, 13, "Database should contain 13 seeded students across colleges including Bennett University")

    def test_matching_score_exact_match(self):
        # Candidate 1: Rohan Sharma (Night Owl, CGPA 8.8, Strong: DSA, Weak: Digital Electronics)
        # Test User: Night Owl, CGPA 8.8, Strong: Digital Electronics, Weak: DSA
        # Expected:
        # Schedule: +40
        # CGPA: +30 (delta 0)
        # Skill Swap:
        #   Candidate teaches User (DSA == DSA): +15
        #   User teaches Candidate (Digital Electronics == Digital Electronics): +15
        # Total = 100
        candidate = {
            "name": "Rohan Sharma",
            "study_hours": "Night Owl",
            "target_cgpa": 8.8,
            "strong_subject": "Data Structures & Algorithms",
            "weak_subject": "Digital Electronics"
        }
        user_profile = {
            "name": "Test User",
            "study_hours": "Night Owl",
            "target_cgpa": 8.8,
            "strong_subject": "Digital Electronics",
            "weak_subject": "Data Structures & Algorithms"
        }
        score, breakdown, tags = calculate_match_score(user_profile, candidate)
        self.assertEqual(score, 100.0)
        self.assertEqual(breakdown["schedule_pts"], 40.0)
        self.assertEqual(breakdown["cgpa_pts"], 30.0)
        self.assertEqual(breakdown["skill_pts"], 30.0)

    def test_matching_partial_and_tags(self):
        # Different schedule, delta CGPA = 1.0, 1-way skill swap
        candidate = {
            "name": "Ananya Iyer",
            "study_hours": "Early Bird",
            "target_cgpa": 9.2,
            "strong_subject": "Calculus",
            "weak_subject": "Operating Systems"
        }
        user_profile = {
            "name": "Aditya",
            "study_hours": "Night Owl",
            "target_cgpa": 8.2, # diff = 1.0 -> 30 - (10 * 1.0) = 20.0 pts
            "strong_subject": "Operating Systems", # teaches candidate: +15
            "weak_subject": "Digital Logic"        # candidate has Calculus: 0
        }
        score, breakdown, tags = calculate_match_score(user_profile, candidate)
        self.assertEqual(breakdown["schedule_pts"], 0.0)
        self.assertEqual(breakdown["cgpa_pts"], 20.0)
        self.assertEqual(breakdown["skill_pts"], 15.0)
        self.assertEqual(score, 35.0)

    def test_canonical_schema_and_matching(self):
        # Test using canonical column names: time_pref, target_gpa, teach_subject, need_subject, reputation_score
        candidate = {
            "name": "Diya Kashyap",
            "time_pref": "Morning",
            "target_gpa": 9.2,
            "teach_subject": "Data Structures",
            "need_subject": "Digital Logic",
            "reputation_score": 98
        }
        user_profile = {
            "name": "Aryan Singhal",
            "time_pref": "Morning",
            "target_gpa": 8.7, # diff = 0.5 -> 30 - 5.0 = 25.0
            "teach_subject": "Digital Logic",  # matches candidate need -> +15
            "need_subject": "Data Structures", # matches candidate teach -> +15
            "reputation_score": 95
        }
        score, breakdown, tags = calculate_match_score(user_profile, candidate)
        self.assertEqual(breakdown["schedule_pts"], 40.0)
        self.assertEqual(breakdown["cgpa_pts"], 25.0)
        self.assertEqual(breakdown["skill_pts"], 30.0)
        self.assertEqual(score, 95.0)

    def test_deploy_ready_files(self):
        # Verify Procfile and requirements.txt exist and are properly configured
        base_dir = os.path.dirname(__file__)
        procfile_path = os.path.join(base_dir, "Procfile")
        req_path = os.path.join(base_dir, "requirements.txt")
        self.assertTrue(os.path.exists(procfile_path), "Procfile must exist for deployment")
        self.assertTrue(os.path.exists(req_path), "requirements.txt must exist for deployment")
        with open(procfile_path, "r") as f:
            content = f.read()
            self.assertIn("web: gunicorn app:app", content)
        with open(req_path, "r") as f:
            content = f.read()
            self.assertIn("gunicorn", content)
            self.assertIn("flask", content)

    def test_api_match(self):
        payload = {
            "name": "Aditya Kumar",
            "section": "CSE-A",
            "study_hours": "Night Owl",
            "target_cgpa": 8.6,
            "strong_subject": "Data Structures & Algorithms",
            "weak_subject": "Operating Systems"
        }
        res = self.client.post("/api/match", data=json.dumps(payload), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        squad = data["squad"]
        self.assertEqual(len(squad["top_candidates"]), 3, "Squad must include top 3 candidates")
        self.assertIn("synergy_score", squad)

    def test_peer_review(self):
        # Review Rohan (id=1)
        review_data = {
            "student_id": 1,
            "reviewer_name": "Aditya",
            "punctual": True,
            "focused": True,
            "rating": 5
        }
        res = self.client.post("/api/review", data=json.dumps(review_data), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertIn("new_score", data)

    def test_create_student_profile(self):
        new_profile = {
            "name": "Tanvi Joshi",
            "section": "CSE-B",
            "study_hours": "Early Bird",
            "target_cgpa": 9.1,
            "strong_subject": "Mathematics & Linear Algebra",
            "weak_subject": "Computer Networks",
            "bio": "Competitive math Olympiad finalist."
        }
        res = self.client.post("/api/students", data=json.dumps(new_profile), content_type="application/json")
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["student"]["name"], "Tanvi Joshi")

        # Verify candidate count increased to 14
        res_list = self.client.get("/api/candidates")
        data_list = res_list.get_json()
        self.assertEqual(data_list["count"], 14)

    def test_selective_college_matching(self):
        # Match student from Bennett University
        bennett_user = {
            "name": "Aayush Sharma",
            "college": "Bennett University",
            "section": "CSE-AI",
            "study_hours": "Night Owl",
            "target_cgpa": 8.7,
            "strong_subject": "Operating Systems",
            "weak_subject": "Machine Learning & AI"
        }
        res_bennett = self.client.post("/api/match", data=json.dumps(bennett_user), content_type="application/json")
        self.assertEqual(res_bennett.status_code, 200)
        squad_bennett = res_bennett.get_json()["squad"]
        self.assertEqual(len(squad_bennett["top_candidates"]), 3)
        for cand in squad_bennett["top_candidates"]:
            self.assertEqual(cand["college"], "Bennett University", "Every matched peer must belong to Bennett University")

        # Match student from Apex Institute of Technology
        apex_user = {
            "name": "Aditya Kumar",
            "college": "Apex Institute of Technology",
            "section": "CSE-A",
            "study_hours": "Night Owl",
            "target_cgpa": 8.5,
            "strong_subject": "Data Structures & Algorithms",
            "weak_subject": "Operating Systems"
        }
        res_apex = self.client.post("/api/match", data=json.dumps(apex_user), content_type="application/json")
        self.assertEqual(res_apex.status_code, 200)
        squad_apex = res_apex.get_json()["squad"]
        for cand in squad_apex["top_candidates"]:
            self.assertEqual(cand["college"], "Apex Institute of Technology", "Every matched peer must belong to Apex Institute of Technology")

        # Match student from Metro Tech University
        metro_user = {
            "name": "Riya Sen",
            "college": "Metro Tech University",
            "section": "CSE-B",
            "study_hours": "Early Bird",
            "target_cgpa": 9.0,
            "strong_subject": "Operating Systems",
            "weak_subject": "Mathematics & Linear Algebra"
        }
        res_metro = self.client.post("/api/match", data=json.dumps(metro_user), content_type="application/json")
        self.assertEqual(res_metro.status_code, 200)
        squad_metro = res_metro.get_json()["squad"]
        for cand in squad_metro["top_candidates"]:
            self.assertEqual(cand["college"], "Metro Tech University", "Every matched peer must belong to Metro Tech University")

    def test_squad_messaging(self):
        # 1. Form a Bennett University squad
        user = {
            "name": "Kabir Mehra",
            "college": "Bennett University",
            "section": "EB04",
            "study_hours": "Night Owl",
            "target_cgpa": 8.9,
            "strong_subject": "Data Structures & Algorithms",
            "weak_subject": "Operating Systems"
        }
        res = self.client.post("/api/match", data=json.dumps(user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        squad = data["squad"]
        squad_id = squad["squad_id"]
        self.assertTrue(squad_id.startswith("squad_bennettuniversity"))
        
        # 2. Check auto-initialized greetings in lounge
        initial_messages = data.get("initial_messages", [])
        self.assertGreaterEqual(len(initial_messages), 2, "Squad lounge should have seeded welcome greetings")
        
        # 3. Post a message to lounge
        msg_payload = {
            "channel": "lounge",
            "sender_name": "Kabir Mehra",
            "sender_avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Kabir",
            "sender_role": "Squad Lead (You)",
            "message": "Hey team, when are we starting our first study sprint?"
        }
        post_res = self.client.post(f"/api/squad/{squad_id}/messages", data=json.dumps(msg_payload), content_type="application/json")
        self.assertEqual(post_res.status_code, 201)
        saved_msg = post_res.get_json()["message"]
        self.assertEqual(saved_msg["message"], "Hey team, when are we starting our first study sprint?")

        # 4. Fetch messages from lounge channel
        get_res = self.client.get(f"/api/squad/{squad_id}/messages?channel=lounge")
        self.assertEqual(get_res.status_code, 200)
        messages = get_res.get_json()["messages"]
        self.assertTrue(any(m["message"] == "Hey team, when are we starting our first study sprint?" for m in messages))

        # 5. Post a 1-on-1 Direct Message to a specific peer
        peer1_id = squad["top_candidates"][0]["id"]
        dm_channel = f"dm_{peer1_id}"
        dm_payload = {
            "channel": dm_channel,
            "sender_name": "Kabir Mehra",
            "sender_avatar": "https://api.dicebear.com/7.x/bottts/svg?seed=Kabir",
            "sender_role": "Squad Lead (You)",
            "message": "Hey! Can you share your notes for our next sprint?"
        }
        dm_res = self.client.post(f"/api/squad/{squad_id}/messages", data=json.dumps(dm_payload), content_type="application/json")
        self.assertEqual(dm_res.status_code, 201)

        # 6. Verify channel isolation (DM channel only contains the DM, not lounge messages)
        dm_get_res = self.client.get(f"/api/squad/{squad_id}/messages?channel={dm_channel}")
        dm_messages = dm_get_res.get_json()["messages"]
        self.assertEqual(len(dm_messages), 1)
        self.assertEqual(dm_messages[0]["message"], "Hey! Can you share your notes for our next sprint?")

        # 7. Test simulated peer response
        sim_payload = {
            "channel": "lounge",
            "user_message": "When should we meet?",
            "peer_name": "Aryan Singhal",
            "peer_id": peer1_id,
            "peer_strong": "Digital Electronics"
        }
        sim_res = self.client.post(f"/api/squad/{squad_id}/simulate_reply", data=json.dumps(sim_payload), content_type="application/json")
        self.assertEqual(sim_res.status_code, 200)
        sim_msg = sim_res.get_json()["message"]
        self.assertIn("library", sim_msg["message"].lower())

    def test_session_track_filtering(self):
        # 1. Honor-Roll track: should strictly match students with target_gpa >= 8.5 who selected honor_roll
        hr_user = {
            "name": "Pranav Bansal",
            "college": "Bennett University",
            "section": "CSE-A",
            "study_hours": "Early Bird",
            "target_cgpa": 9.0,
            "strong_subject": "Physics",
            "weak_subject": "Calculus",
            "track": "honor_roll"
        }
        res_hr = self.client.post("/api/match", data=json.dumps(hr_user), content_type="application/json")
        self.assertEqual(res_hr.status_code, 200)
        squad_hr = res_hr.get_json()["squad"]
        self.assertEqual(squad_hr["track"], "honor_roll")
        self.assertGreaterEqual(len(squad_hr["top_candidates"]), 2)
        for cand in squad_hr["top_candidates"]:
            cand_gpa = float(cand.get("target_gpa") or cand.get("target_cgpa") or 0.0)
            self.assertEqual(cand.get("track"), "honor_roll", f"{cand['name']} must be honor_roll")
            self.assertGreaterEqual(cand_gpa, 8.5, f"{cand['name']} GPA must be >= 8.5")

        # 2. Exchange track: matches candidates normally
        ex_user = {
            "name": "Arjun Das",
            "college": "Bennett University",
            "section": "CSE-B",
            "study_hours": "Night Owl",
            "target_cgpa": 8.0,
            "strong_subject": "Data Structures & Algorithms",
            "weak_subject": "Digital Logic",
            "track": "exchange"
        }
        res_ex = self.client.post("/api/match", data=json.dumps(ex_user), content_type="application/json")
        self.assertEqual(res_ex.status_code, 200)
        squad_ex = res_ex.get_json()["squad"]
        self.assertEqual(squad_ex["track"], "exchange")
        self.assertEqual(len(squad_ex["top_candidates"]), 3)

    def test_group_cohesion_and_pod_roles(self):
        # User with role preference "scribe"
        user = {
            "name": "Siddharth Rao",
            "college": "Bennett University",
            "section": "CSE-AI",
            "study_hours": "Night Owl",
            "target_cgpa": 8.8,
            "strong_subject": "Operating Systems",
            "weak_subject": "Machine Learning & AI",
            "role_preference": "scribe",
            "track": "exchange"
        }
        res = self.client.post("/api/match", data=json.dumps(user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        squad = res.get_json()["squad"]

        # Check group cohesion score is computed
        self.assertIn("group_cohesion_score", squad)
        self.assertIsInstance(squad["group_cohesion_score"], (int, float))
        self.assertGreater(squad["group_cohesion_score"], 0)

        # Check user's preferred role was honored
        self.assertEqual(squad["user"]["assigned_role"], "scribe")

        # Check that all 4 squad members have distinct roles from the 4 standard pod roles
        all_members = [squad["user"]] + squad["top_candidates"]
        self.assertEqual(len(all_members), 4)
        assigned_roles = [m["assigned_role"] for m in all_members]
        expected_roles = {"concept_lead", "scribe", "time_tracker", "resource_lead"}
        self.assertEqual(set(assigned_roles), expected_roles, "All 4 members must have distinct pod roles")

    def test_study_credits_and_checkin(self):
        # Seed student (Diya Kashyap, id=2 in seeded Bennett students)
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students WHERE name = 'Diya Kashyap'")
        diya = dict(cursor.fetchone())
        conn.close()
        diya_id = diya["id"]
        initial_credits = diya["study_credits"]

        # 1. Start sprint: deducts 10-credit deposit
        start_res = self.client.post("/api/session/checkin", data=json.dumps({
            "student_id": diya_id,
            "action": "start"
        }), content_type="application/json")
        self.assertEqual(start_res.status_code, 200)
        data = start_res.get_json()
        self.assertEqual(data["study_credits"], initial_credits - 10)

        # 2. Complete sprint: refunds 10 deposit + 5 bonus
        comp_res = self.client.post("/api/session/checkin", data=json.dumps({
            "student_id": diya_id,
            "action": "complete"
        }), content_type="application/json")
        self.assertEqual(comp_res.status_code, 200)
        self.assertEqual(comp_res.get_json()["study_credits"], initial_credits + 5)

        # 3. Unexcused no-show for experienced user (review_count > 0): forfeits deposit and reduces priority
        # First start another sprint
        self.client.post("/api/session/checkin", data=json.dumps({
            "student_id": diya_id,
            "action": "start"
        }), content_type="application/json")
        # Then trigger unexcused no-show
        noshow_res = self.client.post("/api/session/checkin", data=json.dumps({
            "student_id": diya_id,
            "action": "noshow"
        }), content_type="application/json")
        self.assertEqual(noshow_res.status_code, 200)
        noshow_data = noshow_res.get_json()
        self.assertIn("forfeited", noshow_data["message"].lower())
        self.assertLess(noshow_data["matching_priority"], 1.2)

        # 4. First-time user grace session (review_count == 0)
        fresh_student = add_student({
            "name": "Fresh Student",
            "college": "Apex Institute of Technology",
            "section": "CSE-1",
            "study_hours": "Night Owl",
            "target_cgpa": 8.0,
            "strong_subject": "Python",
            "weak_subject": "Calculus",
            "review_count": 0,
            "study_credits": 50,
            "matching_priority": 1.0
        })
        fresh_id = fresh_student["id"]

        # Start sprint (deduct 10)
        self.client.post("/api/session/checkin", data=json.dumps({
            "student_id": fresh_id,
            "action": "start"
        }), content_type="application/json")
        # Report no-show: first-time grace session should refund deposit and preserve priority
        grace_res = self.client.post("/api/session/checkin", data=json.dumps({
            "student_id": fresh_id,
            "action": "noshow"
        }), content_type="application/json")
        grace_data = grace_res.get_json()
        self.assertEqual(grace_data["study_credits"], 50, "Deposit must be refunded under first-time grace policy")
        self.assertEqual(grace_data["matching_priority"], 1.0, "Priority must not be penalized under grace policy")
        self.assertIn("grace", grace_data["message"].lower())

    def test_verified_mentor_badge(self):
        # 1. Create a student with 14 completed teaching sessions
        mentor_student = add_student({
            "name": "Mentor Candidate",
            "college": "Apex Institute of Technology",
            "section": "CSE-A",
            "study_hours": "Night Owl",
            "target_cgpa": 9.0,
            "strong_subject": "Data Structures & Algorithms",
            "weak_subject": "Operating Systems",
            "review_count": 14,
            "teaching_sessions_completed": 14,
            "verified_mentor": 0
        })
        mentor_id = mentor_student["id"]

        # 2. Submit 15th review meeting all criteria (punctual=True, focused=True, rating=5 >= 4)
        rev_res = self.client.post("/api/review", data=json.dumps({
            "student_id": mentor_id,
            "reviewer_name": "Reviewer",
            "punctual": True,
            "focused": True,
            "rating": 5
        }), content_type="application/json")
        self.assertEqual(rev_res.status_code, 200)
        data = rev_res.get_json()
        self.assertEqual(data["teaching_sessions_completed"], 15)
        self.assertEqual(data["verified_mentor"], 1, "Must achieve verified mentor status at 15 sessions")
        self.assertEqual(data["sessions_taught"], 15)
        self.assertEqual(data["is_mentor"], 1)

        # 3. Verify in candidates list API
        cand_res = self.client.get("/api/candidates?college=Apex%20Institute%20of%20Technology")
        self.assertEqual(cand_res.status_code, 200)
        candidates = cand_res.get_json()["candidates"]
        promoted = next((c for c in candidates if c["id"] == mentor_id), None)
        self.assertIsNotNone(promoted)
        self.assertEqual(promoted["verified_mentor"], 1)
        self.assertEqual(promoted["is_mentor"], 1)
        self.assertEqual(promoted["sessions_taught"], 15)

    def test_micro_sprint_and_expiration(self):
        user = {
            "name": "Kavya Reddy",
            "college": "Bennett University",
            "section": "CSE-B",
            "study_hours": "Early Bird",
            "target_cgpa": 8.5,
            "strong_subject": "Calculus",
            "weak_subject": "Physics",
            "sprint_type": "48hr_exam_prep"
        }
        res = self.client.post("/api/match", data=json.dumps(user), content_type="application/json")
        self.assertEqual(res.status_code, 200)
        squad = res.get_json()["squad"]
        squad_id = squad["squad_id"]

        # Check squad session status via GET /api/squad/<id>
        squad_res = self.client.get(f"/api/squad/{squad_id}")
        self.assertEqual(squad_res.status_code, 200)
        squad_data = squad_res.get_json()
        self.assertEqual(squad_data["status"], "success")
        self.assertEqual(squad_data["session_status"], "active")
        self.assertEqual(squad_data["expired"], False)
        self.assertEqual(squad_data["sprint_type"], "48hr_exam_prep")
        self.assertIn("expires_at", squad_data)
        self.assertIn("time_remaining", squad_data)

    def test_database_migration_idempotency(self):
        # Calling init_db() without force_reset should not drop data and run PRAGMA column additions cleanly
        init_db(force_reset=False)
        init_db(force_reset=False)

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(students)")
        cols = {row["name"] for row in cursor.fetchall()}
        conn.close()

        expected_cols = {
            "id", "name", "college", "section", "time_pref", "study_hours",
            "target_gpa", "target_cgpa", "teach_subject", "strong_subject",
            "need_subject", "weak_subject", "reputation_score", "reliability_score",
            "review_count", "bio", "track", "role_preference", "study_credits",
            "matching_priority", "teaching_sessions_completed", "verified_mentor",
            "sessions_taught", "is_mentor"
        }
        for col in expected_cols:
            self.assertIn(col, cols, f"Column '{col}' must exist in students table after migration")

    def test_verified_mentor_seed_data(self):
        # Must include at least 2 students with sessions_taught >= 15 and is_mentor = 1
        res = self.client.get("/api/candidates")
        self.assertEqual(res.status_code, 200)
        candidates = res.get_json()["candidates"]
        mentors = [c for c in candidates if c.get("sessions_taught", 0) >= 15 and c.get("is_mentor") == 1]
        self.assertGreaterEqual(len(mentors), 2, "Database seed data must include at least 2 verified mentors")

    def test_mentor_certificate_route(self):
        # 1. Fetch candidates to find a verified mentor and a non-mentor
        res = self.client.get("/api/candidates")
        self.assertEqual(res.status_code, 200)
        candidates = res.get_json()["candidates"]
        
        mentor = next((c for c in candidates if c.get("is_mentor") == 1 or c.get("sessions_taught", 0) >= 15), None)
        non_mentor = next((c for c in candidates if c.get("is_mentor") == 0 and c.get("sessions_taught", 0) < 15), None)

        self.assertIsNotNone(mentor, "Must have at least one verified mentor")
        self.assertIsNotNone(non_mentor, "Must have at least one non-mentor")

        # 2. Mentor certificate request should succeed (200 OK)
        cert_res = self.client.get(f"/certificate/{mentor['id']}")
        self.assertEqual(cert_res.status_code, 200)
        html = cert_res.get_data(as_text=True)
        self.assertIn("Verified Peer Mentor Award", html)
        self.assertIn("VibeStudy Academic Network", html)
        self.assertIn(mentor["name"], html)
        self.assertIn("VIBE-CERT-", html)
        self.assertIn("window.print()", html)

        # 3. Non-mentor certificate request should be forbidden (403 Forbidden)
        denied_res = self.client.get(f"/certificate/{non_mentor['id']}")
        self.assertEqual(denied_res.status_code, 403)
        denied_html = denied_res.get_data(as_text=True)
        self.assertIn("Mentor Certification Pending", denied_html)
        self.assertIn("HTTP 403", denied_html)

        # 4. Non-existent student ID should return 404
        not_found_res = self.client.get("/certificate/999999")
        self.assertEqual(not_found_res.status_code, 404)

    def test_instagram_style_profile_dashboard(self):
        # 1. Reset and seed demo students
        init_db(force_reset=True, seed_demo=True)
        
        # 2. Test valid profile endpoint (HTML)
        res = self.client.get("/profile/1")
        self.assertEqual(res.status_code, 200)
        html = res.get_data(as_text=True)
        self.assertIn("Ishaan Malhotra", html)
        self.assertIn("@CSE-AI", html)
        self.assertIn("Study Sprints", html)
        self.assertIn("Hours Studied", html)
        self.assertIn("Mentored", html)
        self.assertIn("Avg Rating", html)
        self.assertIn("Academic Badges", html)
        self.assertIn("Peer Reviews", html)

        # 3. Test API profile endpoint (JSON)
        api_res = self.client.get("/api/profile/1")
        self.assertEqual(api_res.status_code, 200)
        data = api_res.get_json()
        self.assertEqual(data["status"], "success")
        profile = data["profile"]
        self.assertEqual(profile["student"]["name"], "Ishaan Malhotra")
        self.assertGreaterEqual(profile["stats"]["total_sprints"], 2)
        self.assertGreaterEqual(len(profile["sessions"]), 2)
        self.assertGreaterEqual(len(profile["reviews"]), 2)
        self.assertGreaterEqual(len(profile["badges"]), 3)

        # 4. Test Verified Mentor Profile
        mentor_res = self.client.get("/profile/2")
        self.assertEqual(mentor_res.status_code, 200)
        mentor_html = mentor_res.get_data(as_text=True)
        self.assertIn("Verified Mentor", mentor_html)
        self.assertIn("avatar-ring-mentor", mentor_html)

        # 5. Test 404 for non-existent student
        not_found = self.client.get("/profile/999999")
        self.assertEqual(not_found.status_code, 404)

if __name__ == "__main__":
    unittest.main()
