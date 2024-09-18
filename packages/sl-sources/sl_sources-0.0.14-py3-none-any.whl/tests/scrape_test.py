import pytest

from sl_sources.scrape import browser_scrape


@pytest.mark.asyncio
async def test_browser_scrape():
    """
    Run a test scrape on a sample URL.
    """
    print("Scraping...")
    text = await browser_scrape(
        "https://www.nytimes.com/2024/04/29/technology/ai-google-microsoft.html"
    )
    print("Scraped")
    print(text)
