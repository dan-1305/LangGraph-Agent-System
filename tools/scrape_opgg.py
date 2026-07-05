from playwright.sync_api import sync_playwright

def scrape_valorant():
    print("Launching Playwright...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print("Navigating to OP.GG...")
        try:
            page.goto("https://op.gg/vi/valorant/profile/Ch%C6%A1iVui-4340?statQueueId=all", wait_until="networkidle", timeout=30000)
            print("Waiting 5s for client-side rendering...")
            page.wait_for_timeout(5000)
            
            content = page.content()
            if "Checking your browser" in content or "Cloudflare" in content:
                print("FAILED: Blocked by Cloudflare Turnstile.")
            else:
                print("SUCCESS: Bypassed checks.")
                
                try:
                    text_content = page.locator("body").inner_text()
                    print("\n--- EXTRACTED CONTENT ---")
                    # handle printing safe characters
                    print(text_content.encode('utf-8', errors='ignore').decode('utf-8')[:1500])
                except Exception as e:
                    print(f"Cannot get text: {e}")
        except Exception as e:
            print(f"Access error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    scrape_valorant()
