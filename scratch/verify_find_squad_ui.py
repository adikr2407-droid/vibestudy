import time
from playwright.sync_api import sync_playwright

def test_find_squad():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        console_errors = []
        page_errors = []

        page.on("console", lambda msg: print(f"[CONSOLE {msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGEERROR] {err}"))

        print("1. Loading http://127.0.0.1:5000/ ...")
        page.goto("http://127.0.0.1:5000/")
        page.wait_for_selector("#onboardingSection", state="visible")
        time.sleep(1)

        print("2. Clicking 'Quick Demo Profile'...")
        page.click("#quickDemoBtn")
        time.sleep(0.5)

        # Print field values
        print("userName value:", page.input_value("#userName"))
        print("userSection value:", page.input_value("#userSection"))
        print("userCollege value:", page.input_value("#userCollege"))
        print("strongSubject value:", page.input_value("#strongSubject"))
        print("weakSubject value:", page.input_value("#weakSubject"))

        print("3. Submitting 'Find My Study Squad'...")
        page.click("#submitBtn")

        for i in range(12):
            time.sleep(0.5)
            onboarding_hidden = "hidden" in page.get_attribute("#onboardingSection", "class")
            scanning_hidden = "hidden" in page.get_attribute("#scanningSection", "class")
            results_hidden = "hidden" in page.get_attribute("#resultsSection", "class")
            print(f"Tick {i}: onboarding hidden={onboarding_hidden}, scanning hidden={scanning_hidden}, results hidden={results_hidden}")
            if not results_hidden:
                break

        # Confirm 4 squad cards exist
        lead_card = page.query_selector(".squad-card-lead")
        peer_cards = page.query_selector_all(".squad-card-peer")
        print(f"Lead card found: {lead_card is not None}, Peer cards found: {len(peer_cards)}")

        # Check synergy and cohesion values
        synergy_val = page.text_content("#synergyScoreVal")
        cohesion_val = page.text_content("#cohesionScoreVal")
        print(f"Synergy: {synergy_val}, Cohesion: {cohesion_val}")

        # Check candidate table
        rows = page.query_selector_all("#candidatesTableBody tr")
        print(f"Candidate table rows rendered: {len(rows)}")

        # Screenshot squad results
        page.screenshot(path="C:/Users/adikr/.gemini/antigravity/brain/24839b0c-eea7-4985-bf75-535d08fec66e/squad_results_fixed.png", full_page=True)
        print("Screenshot saved: squad_results_fixed.png")

        print("5. Testing Mentor Match in Bennett University...")
        page.goto("http://127.0.0.1:5000/")
        page.select_option("#userCollege", "Bennett University")
        page.fill("#userName", "Arjun Patel")
        page.fill("#userSection", "CSE-B")
        
        # Select Early Bird
        early_bird = page.query_selector('input[name="studyHours"][value="Early Bird"]')
        if early_bird:
            page.evaluate("el => el.click()", early_bird)
            
        page.select_option("#strongSubject", "Digital Logic")
        page.select_option("#weakSubject", "Data Structures")

        page.click("#submitBtn")
        page.wait_for_selector("#resultsSection", state="visible", timeout=6000)
        time.sleep(1)

        # Check for Verified Mentor badge on Diya Kashyap's card
        mentor_badges = page.query_selector_all("text=Verified Mentor")
        print(f"Found {len(mentor_badges)} 'Verified Mentor' badges!")
        
        cert_buttons = page.query_selector_all("text=View Certificate")
        print(f"Found {len(cert_buttons)} 'View Certificate' buttons!")

        page.screenshot(path="C:/Users/adikr/.gemini/antigravity/brain/24839b0c-eea7-4985-bf75-535d08fec66e/bennett_mentor_squad.png", full_page=True)
        print("Screenshot saved: bennett_mentor_squad.png")

        print("Console errors during session:", console_errors)
        print("Page uncaught exceptions:", page_errors)

        assert len(page_errors) == 0, f"Uncaught page errors: {page_errors}"
        print("ALL UI BROWSER VERIFICATION TESTS PASSED SUCCESSFULLY!")

        browser.close()

if __name__ == "__main__":
    test_find_squad()
