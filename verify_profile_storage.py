import os
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\adikr\.gemini\antigravity\brain\24839b0c-eea7-4985-bf75-535d08fec66e"
CHROME_PATH = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

def run_storage_verification():
    print("Starting Profile Storage Verification...")
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

        # 2. Click "Peer Pool" button to open Candidate Pool modal
        print("Opening Peer Pool Directory Modal...")
        page.click("#viewPoolBtn")
        page.wait_for_selector("#peerPoolModal:not(.hidden)", timeout=5000)
        time.sleep(1)

        # Screenshot: Candidate Directory Modal
        shot1 = os.path.join(ARTIFACT_DIR, "7_candidate_pool_directory.png")
        page.screenshot(path=shot1)
        print(f"Saved: {shot1}")

        # 3. Close Directory and match a squad that needs Digital Electronics
        page.click("#peerPoolModal button:has-text('Close Directory')")
        page.wait_for_selector("#peerPoolModal", state="hidden", timeout=5000)
        time.sleep(0.5)

        print("Testing matching with the newly stored profile (Neha Varma)...")
        # Vikram: Night Owl, 8.9 CGPA, Strong: DBMS, Weak: Digital Electronics
        page.fill("#userName", "Vikram Rathore")
        page.fill("#userSection", "CSE-A")
        
        # Click the Night Owl card
        page.click(".study-hour-card:has(input[value='Night Owl'])")
        
        page.fill("#cgpaSlider", "8.9")
        page.evaluate("document.getElementById('cgpaSlider').dispatchEvent(new Event('input'))")
        
        page.select_option("#strongSubject", "Database Management Systems")
        page.select_option("#weakSubject", "Digital Electronics")
        
        page.click("#submitBtn")
        page.wait_for_selector("#resultsSection:not(.hidden)", timeout=10000)
        time.sleep(2)

        # Screenshot: Matched squad showing Neha Varma!
        shot4 = os.path.join(ARTIFACT_DIR, "10_matched_with_new_candidate.png")
        page.screenshot(path=shot4)
        print(f"Saved: {shot4}")

        browser.close()
        print("Profile storage and matching verification complete!")

if __name__ == "__main__":
    run_storage_verification()
