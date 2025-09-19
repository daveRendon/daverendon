#!/usr/bin/env python3
"""
Automate a manual sync request on the SociableKIT website.

This script uses Selenium WebDriver to open the SociableKIT widget page,
authenticate using credentials provided via environment variables and
click the "Request sync" control.  Set the SOCIALKIT_EMAIL and
SOCIALKIT_PASSWORD secrets in your repository.

Requirements: selenium, webdriver-manager, and Chrome on the runner.
"""

import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def main() -> int:
    email = os.environ.get("SOCIALKIT_EMAIL")
    password = os.environ.get("SOCIALKIT_PASSWORD")
    if not email or not password:
        print("Environment variables SOCIALKIT_EMAIL and SOCIALKIT_PASSWORD must be set.")
        return 1

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    from selenium.webdriver.chrome.service import Service
    driver_path = ChromeDriverManager().install()
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(60)

    try:
        widget_url = "https://www.sociablekit.com/app/users/widgets/update_embed/73691/#basic"
        driver.get(widget_url)

        # Login if the form appears
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
            pass

        # Wait for asynchronous content to load
        time.sleep(15)
        print("🔎 Looking for sync button…")

        def find_and_click_request_button() -> bool:
            """
            Recursively search for any element containing 'Request sync' and click it.
            """
            try:
                elem = driver.find_element(
                    By.XPATH,
                    "//*[contains(translate(normalize-space(text()), "
                    "'ABCDEFGHIJKLMNOPQRSTUVWXYZ','abcdefghijklmnopqrstuvwxyz'), 'request sync')]",
                )
                driver.execute_script("arguments[0].click();", elem)
                return True
            except Exception:
                pass
            frames = driver.find_elements(By.TAG_NAME, "iframe")
            for frame in frames:
                driver.switch_to.frame(frame)
                if find_and_click_request_button():
                    return True
                driver.switch_to.parent_frame()
            return False

        if not find_and_click_request_button():
            with open("page_dump.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("❌ Could not find the 'Request sync' button anywhere.")
            return 1

        # Optional wait for confirmation
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//*[contains(., 'Sync request') and contains(., 'received')]")
                )
            )
        except Exception:
            pass
        print("✅ Sync request submitted successfully.")
    finally:
        driver.quit()
    return 0

if __name__ == "__main__":
    sys.exit(main())
