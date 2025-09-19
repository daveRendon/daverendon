#!/usr/bin/env python3
"""
Automate a manual sync request on the SociableKIT website.

This script uses Selenium WebDriver to open the SociableKIT widget page,
authenticate using credentials provided via environment variables and
click the "Request sync" button. It is intended to be run in a headless
environment such as a GitHub Actions runner.  You must set the
SOCIALKIT_EMAIL and SOCIALKIT_PASSWORD secrets in your repository so
that the script can log in.

Usage:
    python sync_sociablekit.py

Requirements:
    - selenium
    - webdriver-manager (to automatically install ChromeDriver)
    - Google Chrome available on PATH (GitHub runners come with it)

Note: This script provides a basic example.  Depending on changes to
the SociableKIT login page, you may need to adjust the element
selectors or add waits. Always test locally before relying on
automation.
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

    # Configure headless Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    driver.set_page_load_timeout(60)

    try:
        # Navigate to the widget page (this redirects to login if not authenticated)
        widget_url = "https://www.sociablekit.com/app/users/widgets/update_embed/73691/#basic"
        driver.get(widget_url)

        # Wait for either the login form or the main page to load
        try:
            # Check if login email field is present
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='email']"))
            )
            # Fill in credentials
            email_field.send_keys(email)
            password_field = driver.find_element(By.CSS_SELECTOR, "input[type='password']")
            password_field.send_keys(password)
            # Submit the login form
            submit_btn = driver.find_element(By.XPATH, "//button[contains(., 'Sign in')]")
            submit_btn.click()
            # Wait for redirect back to the widget page
            WebDriverWait(driver, 30).until(
                EC.url_contains("update_embed/73691")
            )
        except Exception:
            # If login elements are not found, assume already logged in
            pass

        # Wait until "Request sync" button is clickable
        request_btn = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Request sync')]"))
        )
        request_btn.click()

        # Optionally wait for confirmation modal
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(., 'Sync request received')]"))
        )
        print("Sync request submitted successfully.")

    finally:
        driver.quit()
    return 0


if __name__ == "__main__":
    sys.exit(main())
