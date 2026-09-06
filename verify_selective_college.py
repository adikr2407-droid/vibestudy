import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\adikr\.gemini\antigravity\brain\24839b0c-eea7-4985-bf75-535d08fec66e"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run_college_verification():
    print("Starting Selective College Verification...")
    with sync_playwright() as p:
        browser = p.chromium.launch(
            executable_path=CHROME_PATH,
            headless=True
        )
        context = browser.new_context(viewport={"width": 1280, "height": 900})
        page = context.new_page()

        # 1. Load Homepage
        print("Navigating to http://127.0.0.1:5000 ...")
        page.goto("http://127.0.0.1:5000", wait_until="networkidle")
        time.sleep(1)

        # 2. Select College: "Metro Tech University"
        print("Selecting Metro Tech University in onboarding form...")
        page.select_option("#userCollege", "Metro Tech University")
        page.fill("#userName", "Riya Sen")
        page.fill("#userSection", "CSE-B")
        
        # Early Bird
        page.click(".study-hour-card:has(input[value='Early Bird'])")

        # CGPA 9.1
        page.fill("#cgpaSlider", "9.1")
        page.evaluate("document.getElementById('cgpaSlider').dispatchEvent(new Event('input'))")

        # Strong: Operating Systems, Weak: Mathematics & Linear Algebra
        page.select_option("#strongSubject", "Operating Systems")
        page.select_option("#weakSubject", "Mathematics & Linear Algebra")

        # Submit Match
        print("Submitting match request for Metro Tech University student...")
        page.click("#submitBtn")
        page.wait_for_selector("#resultsSection:not(.hidden)", timeout=10000)
        time.sleep(1.5)

        # Verify squad college badge
        college_badge_text = page.inner_text("#squadCollegeBadge")
        print(f"Squad Verified Campus Badge: {college_badge_text}")
        assert "Metro Tech" in college_badge_text, f"Expected Metro Tech in badge, got {college_badge_text}"

        # Verify all peer cards belong to Metro Tech University
        peer_cards = page.query_selector_all(".squad-card-peer")
        print(f"Found {len(peer_cards)} matched peers")
        for i, card in enumerate(peer_cards):
            card_text = card.inner_text()
            print(f"Peer {i+1} Text contains Metro Tech: {'Metro Tech University' in card_text}")
            assert "Metro Tech University" in card_text, f"Peer {i+1} is not from Metro Tech University!"

        # Screenshot: Metro Tech University Squad
        shot1 = os.path.join(ARTIFACT_DIR, "11_selective_college_metro_squad.png")
        page.screenshot(path=shot1)
        print(f"Saved: {shot1}")

        # 3. Open Peer Pool Modal and test College Filter tabs
        print("Opening Peer Pool Directory Modal...")
        page.click("#viewPoolBtn")
        page.wait_for_selector("#peerPoolModal:not(.hidden)", timeout=5000)
        time.sleep(1)

        # Click "Metro Tech University" filter tab
        print("Clicking 'Metro Tech University' filter tab in Directory...")
        page.click("button.pool-filter-btn:has-text('Metro Tech University')")
        time.sleep(1)

        # Screenshot: Peer Pool filtered by Metro Tech
        shot2 = os.path.join(ARTIFACT_DIR, "12_peer_pool_college_filter.png")
        page.screenshot(path=shot2)
        print(f"Saved: {shot2}")

        browser.close()
        print("Selective college verification completed successfully!")

if __name__ == "__main__":
    run_college_verification()
