#!/usr/bin/env python3
"""
Use Playwright to automate a manual sync request on the SociableKIT website.

This script launches a headless Chromium browser via Playwright, navigates
to the SociableKIT widget page, logs in using credentials from environment
variables, and clicks the "Request sync" control. Playwright's robust
handling of frames and shadow DOM should make it more reliable than
Selenium in environments like GitHub Actions.

Before running this script you must:

1. Install Playwright and its browser dependencies:
   pip install playwright
   playwright install --with-deps

2. Set the environment variables SOCIALKIT_EMAIL and SOCIALKIT_PASSWORD
   with your SociableKIT credentials.

3. (Optional) Adjust timeouts if the page loads slowly.
"""

import asyncio
import os
import sys
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError

async def run() -> int:
    email = os.environ.get("SOCIALKIT_EMAIL")
    password = os.environ.get("SOCIALKIT_PASSWORD")
    if not email or not password:
        print("SOCIALKIT_EMAIL and SOCIALKIT_PASSWORD environment variables must be set.")
        return 1

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        widget_url = "https://www.sociablekit.com/app/users/widgets/update_embed/73691/#basic"
        print("Navigating to widget page…")
        await page.goto(widget_url, wait_until="domcontentloaded")

        # Attempt to find login fields. If they exist, fill them in.
        try:
            await page.fill("input[type=email]", email, timeout=10000)
            await page.fill("input[type=password]", password, timeout=5000)
            await page.click("button:has-text('Sign in')", timeout=5000)
            # Wait for redirect back to the widget page
            await page.wait_for_url(lambda url: "update_embed/73691" in url, timeout=30000)
        except PlaywrightTimeoutError:
            # Login inputs not found; assume already logged in
            pass

        # Wait for the "Request sync" control to be available
        try:
            await page.wait_for_selector("text=Request sync", timeout=60000)
            # Use locator to handle frames/shadow DOM
            sync_button = page.locator("text=Request sync")
            await sync_button.click()
            print("✅ Sync request clicked.")
        except PlaywrightTimeoutError:
            print("❌ Could not find the 'Request sync' control on the page.")
            # Save page content for debugging
            html = await page.content()
            with open("page_dump_playwright.html", "w", encoding="utf-8") as f:
                f.write(html)
            return 1
        finally:
            await browser.close()
    return 0

if __name__ == "__main__":
    exit_code = asyncio.run(run())
    sys.exit(exit_code)
