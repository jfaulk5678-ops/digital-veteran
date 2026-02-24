import asyncio
import json
from datetime import datetime

from playwright.async_api import async_playwright


class SimpleCompetitorScraper:
    def __init__(self):
        self.results = []

    async def scrape_competitor(self, url, search_terms):
        """Simple competitor scraper using Playwright directly"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            try:
                print(f"Scraping: {url}")
                await page.goto(url, wait_until="networkidle")

                # Get page content
                text_content = await page.inner_text("body")

                # Look for gaps based on search terms
                gaps_found = []
                for term in search_terms:
                    if term.lower() in text_content.lower():
                        # Get some context around the term
                        index = text_content.lower().find(term.lower())
                        context_start = max(0, index - 50)
                        context_end = min(len(text_content), index + len(term) + 50)
                        context = text_content[context_start:context_end]

                        gaps_found.append(
                            {"term": term, "context": context.strip(), "url": url}
                        )

                result = {
                    "url": url,
                    "timestamp": datetime.now().isoformat(),
                    "content_length": len(text_content),
                    "gaps_found": gaps_found,
                    "search_terms_matched": len(gaps_found),
                }

                self.results.append(result)
                print(f"Found {len(gaps_found)} matches on {url}")
                return result

            except Exception as e:
                print(f"Error scraping {url}: {e}")
                return None
            finally:
                await browser.close()

    async def scrape_multiple(self, urls, search_terms):
        """Scrape multiple competitors"""
        tasks = [self.scrape_competitor(url, search_terms) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [r for r in results if r is not None and not isinstance(r, Exception)]


# Test function
async def test_scraper():
    scraper = SimpleCompetitorScraper()

    competitors = [
        "https://www.salesforce.com",
        "https://www.hubspot.com",
        "https://www.zoho.com",
    ]

    search_terms = ["small business", "startup", "affordable", "easy to use"]

    print("Starting competitor analysis...")
    results = await scraper.scrape_multiple(competitors, search_terms)

    print(f"\nScraped {len(results)} competitors")
    for result in results:
        print(f"{result['url']}: {result['search_terms_matched']} terms matched")

    # Save results
    with open("data/scrapes/first_test.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to data/scrapes/first_test.json")
    return results


if __name__ == "__main__":
    results = asyncio.run(test_scraper())
