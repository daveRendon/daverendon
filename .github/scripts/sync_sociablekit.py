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


def wait_and_click(driver, xpath: str, timeout: int = 30) -> bool:
    """Wait for an element to be clickable and click it."""
    try:
        elem = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, xpath))
        )
        elem.click()
        return True
    except Exception:
        return False


def main() -> int:
    email = os.environ.get("SOCIALKIT_EMAIL")
    password = os.environ.get("SOCIALKIT_PASSWORD")
    if not email or not password:
        print("❌ SOCIALKIT_EMAIL and SOCIALKIT_PASSWORD must be set.")
        return 1

    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # newer headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    driver.set_page_load_timeout(60)

    try:
        widget_url = "https://www.sociablekit.com/app/users/widgets/update_embed/73691/#basic"
        driver.get(widget_url)

        # Try login if required
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            email_field.send_keys(email)
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys(password)

            submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Sign in')]")
            submit_btn.click()

            WebDriverWait(driver, 30).until(
                EC.url_contains("update_embed/73691")
            )
        except Exception:
            pass  # assume already logged in

        # Try to click "Request sync"
        print("🔎 Looking for sync button...")

        sync_xpaths = [
            "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'request sync')]",
            "//button[contains(., 'Request Sync')]",
            "//button[contains(., 'Sync')]",
            "//a[contains(., 'Request sync')]",
        ]

        clicked = False
        for xp in sync_xpaths:
            if wait_and_click(driver, xp, timeout=30):
                clicked = True
                break

        # If not found, maybe inside an iframe
        if not clicked:
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            if iframes:
                print(f"🌐 Found {len(iframes)} iframe(s). Trying inside first one...")
                driver.switch_to.frame(iframes[0])
                for xp in sync_xpaths:
                    if wait_and_click(driver, xp, timeout=15):
                        clicked = True
                        break
                driver.switch_to.default_content()

        if not clicked:
            print("❌ Could not find the 'Request sync' button.")
            return 1

        # Confirmation message
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Sync request received')]"))
            )
            print("✅ Sync request submitted successfully.")
        except Exception:
            print("⚠️ Sync button clicked, but no confirmation message detected.")

    finally:
        driver.quit()

    return 0


if __name__ == "__main__":
    sys.exit(main())
