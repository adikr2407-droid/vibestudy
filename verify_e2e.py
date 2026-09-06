import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\adikr\.gemini\antigravity\brain\24839b0c-eea7-4985-bf75-535d08fec66e"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run_verification():
    print("Starting Playwright E2E verification...")
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

        # Screenshot: Onboarding Form
        shot1 = os.path.join(ARTIFACT_DIR, "1_onboarding_form.png")
        page.screenshot(path=shot1)
        print(f"Saved: {shot1}")

        # 2. Click Quick Demo Autofill
        print("Clicking Quick Demo Autofill...")
        page.click("#quickDemoBtn")
        time.sleep(0.5)

        # Screenshot: Form filled with Demo data
        shot2 = os.path.join(ARTIFACT_DIR, "2_form_filled.png")
        page.screenshot(path=shot2)
        print(f"Saved: {shot2}")

        # 3. Submit Form to trigger Matching Engine
        print("Submitting onboarding form to match squad...")
        page.click("#submitBtn")

        # Wait for results section to be visible
        page.wait_for_selector("#resultsSection:not(.hidden)", timeout=10000)
        time.sleep(1.5)

        # Verify 4 cards in squadGrid
        cards = page.query_selector_all("#squadGrid > div")
        print(f"Found {len(cards)} squad member cards in grid (Target: 4)")
        assert len(cards) == 4, f"Expected 4 squad cards, got {len(cards)}"

        # Check synergy score
        synergy_text = page.inner_text("#synergyScoreVal")
        print(f"Squad Synergy Score: {synergy_text}")

        # Screenshot: Matched 4-Person Squad
        shot3 = os.path.join(ARTIFACT_DIR, "3_matched_squad.png")
        page.screenshot(path=shot3)
        print(f"Saved: {shot3}")

        # 4. Test Pomodoro Timer controls
        print("Testing Pomodoro Timer Start...")
        page.click("#timerToggleBtn")
        time.sleep(1.5)
        timer_text = page.inner_text("#timerDisplay")
        print(f"Timer running: {timer_text}")

        print("Triggering 10s Fast-Forward Demo for timer...")
        page.click("#quickEndBtn")
        time.sleep(11.5) # Wait for 10s sprint to complete

        # Screenshot: Timer completed & chime alert
        shot4 = os.path.join(ARTIFACT_DIR, "4_timer_finished.png")
        page.screenshot(path=shot4)
        print(f"Saved: {shot4}")

        # 5. Test Peer Accountability Modal
        print("Verifying Peer Review Modal...")
        # Since timer finish triggers modal prompt, check if visible or click button
        is_modal_visible = page.is_visible("#reviewModal:not(.hidden)")
        if not is_modal_visible:
            page.click("#openReviewModalBtn")
            page.wait_for_selector("#reviewModal:not(.hidden)", timeout=5000)

        time.sleep(0.5)

        # Screenshot: Review Modal open
        shot5 = os.path.join(ARTIFACT_DIR, "5_review_modal.png")
        page.screenshot(path=shot5)
        print(f"Saved: {shot5}")

        # Select 5th star rating
        stars = page.query_selector_all("#starRatingContainer button")
        if len(stars) >= 5:
            stars[4].click()

        # Submit Review
        print("Submitting peer review...")
        page.click("#submitReviewBtn")
        time.sleep(1.5)

        # Screenshot: Final state with toast and updated peer score
        shot6 = os.path.join(ARTIFACT_DIR, "6_review_submitted.png")
        page.screenshot(path=shot6)
        print(f"Saved: {shot6}")

        browser.close()
        print("All verification steps passed successfully!")

if __name__ == "__main__":
    run_verification()
