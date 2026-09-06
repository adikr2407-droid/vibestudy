import unittest
import json
import os
from database import init_db, get_db
from matching import calculate_match_score, find_squad
from app import app

class TestVibeStudy(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        init_db(force_reset=True)

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

if __name__ == "__main__":
    unittest.main()
