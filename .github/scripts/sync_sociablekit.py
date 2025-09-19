#!/usr/bin/env python3
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager


def wait_and_click(driver, xpath: str, timeout: int = 10) -> bool:
    """Wait for an element to be clickable and click it."""
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elem.click()
        return True
    except Exception:
        return False


def search_iframes(driver, sync_xpaths) -> bool:
    """
    Recursively search through all iframes for the sync button.
    Returns True if found and clicked.
    """
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    print(f"🌐 Found {len(iframes)} iframe(s) at this level.")

    for idx, frame in enumerate(iframes):
        driver.switch_to.frame(frame)
        print(f"➡️ Entering iframe {idx+1}/{len(iframes)}")

        # Try each candidate XPath
        for xp in sync_xpaths:
            if wait_and_click(driver, xp, timeout=5):
                print(f"✅ Found and clicked button using XPath: {xp}")
                return True

        # Recurse into nested iframes
        if search_iframes(driver, sync_xpaths):
            return True

        driver.switch_to.parent_frame()  # back out if not found

    return False


def main() -> int:
    email = os.environ.get("SOCIALKIT_EMAIL")
    password = os.environ.get("SOCIALKIT_PASSWORD")
    if not email or not password:
        print("❌ SOCIALKIT_EMAIL and SOCIALKIT_PASSWORD must be set.")
        return 1

    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(60)

    try:
        widget_url = "https://www.sociablekit.com/app/users/widgets/update_embed/73691/#basic"
        driver.get(widget_url)

        # Try login if required
        try:
            email_field = WebDriverWait(driver, 8).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            email_field.send_keys(email)
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys(password)

            submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Sign in')]")
            submit_btn.click()

            WebDriverWait(driver, 20).until(
                EC.url_contains("update_embed/73691")
            )
        except Exception:
            pass  # assume already logged in

        print("🔎 Looking for sync button...")

        sync_xpaths = [
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'request sync')]",
            "//button[contains(., 'Request Sync')]",
            "//button[contains(., 'Sync')]",
            "//a[contains(., 'Request sync')]",
        ]

        found = False
        # First, try root page
        for xp in sync_xpaths:
            if wait_and_click(driver, xp, timeout=5):
                found = True
                break

        # If not, dive into iframes
        if not found:
            found = search_iframes(driver, sync_xpaths)

        if not found:
            print("❌ Could not find the 'Request sync' button anywhere.")
            # Dump source for debugging
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("💾 Saved current page HTML to page_dump.html")
            return 1

        # Wait for confirmation
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Sync request received')]"))
            )
            print("✅ Sync request submitted successfully.")
        except Exception:
            print("⚠️ Sync button clicked, but no confirmation detected.")

    finally:
        driver.quit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
