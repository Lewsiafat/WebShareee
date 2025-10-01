import asyncio
from playwright.async_api import async_playwright, expect

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Navigate to the running application
        await page.goto("http://localhost:8080/")

        # Wait for the main layout to be visible, specifically the brand logo in the sidebar
        await expect(page.locator(".brand-logo .logo-text")).to_have_text("Static Web")

        # Verify that the new sidebar navigation is present
        await expect(page.get_by_role("menuitem", name="Home")).to_be_visible()

        # Verify the dark mode switch is now in the sidebar footer
        await expect(page.locator(".aside-footer .el-switch")).to_be_visible()

        # Verify the new footer with social links is present
        await expect(page.get_by_label("Github Link")).to_be_visible()

        # Take a screenshot for visual confirmation
        await page.screenshot(path="jules-scratch/verification/verification.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())