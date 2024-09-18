import asyncio
import json
import os
import random
import sys
from pathlib import Path
from typing import List, Set, Optional, Tuple

from bs4 import BeautifulSoup, NavigableString
from playwright.async_api import Page, Browser


def get_proxy():
    print("Getting proxy")
    # if proxies.json doesn't exist, return None
    if not Path("proxies.json").exists():
        return None

    # load proxies.json
    with open("proxies.json") as f:
        proxies = json.load(f)

    # select a random proxy
    proxy = random.choice(proxies)

    # format the proxy for Playwright
    proxy_url = f"{proxy['ip']}:{proxy['port']}"

    return {
        "server": proxy_url,
        # Optionally, if the proxy requires authentication, you can include "username" and "password"
        # "username": proxy.get("username"),
        # "password": proxy.get("password"),
    }


# Lists of keywords and elements to be blacklisted during scraping
link_blacklist: List[str] = [
    "home",
    "next",
    "about us",
    "contact",
    "log in",
    "account",
    "sign",
    "sign up",
    "sign in",
    "sign out",
    "privacy",
    "close",
    "privacy policy",
    "terms of service",
    "terms and conditions",
    "terms",
    "conditions",
    "privacy",
    "legal",
    "guidelines",
    "filter",
    "theme",
    "english",
    "accessibility",
    "authenticate",
    "join",
    "edition",
    "subscribe",
    "news",
    "home",
    "blog",
    "jump to",
    "español",
    "world",
    "europe",
    "politics",
    "profile",
    "election",
    "health",
    "business",
    "tech",
    "sports",
    "advertise",
    "advertising",
    "ad",
    "banner",
    "sponsor",
    "promotion",
    "promoted",
]

element_blacklist: List[str] = [
    "sidebar",
    "nav",
    "footer",
    "header",
    "menu",
    "account",
    "login",
    "form",
    "search",
    "advertisement",
    "masthead",
    "popup",
    "overlay",
    "floater",
    "modal",
    "noscript",
    "iframe",
    "script",
    "style",
    "head",
    "meta",
]


def _check_for_playwright() -> Path:
    """
    Check for Playwright installation and install if not present.

    This function checks if the Playwright browser (Chromium) is installed on the system.
    If not found, it installs it. It then returns the path to the browser executable.

    Returns
    -------
    Path
        The path to the Chromium browser executable.

    Notes
    -----
    This function is platform-aware and handles differences between Windows, macOS, and Linux.
    """
    if sys.platform.startswith("win"):
        browsers_path = Path(os.getenv("LOCALAPPDATA", "")) / "ms-playwright"
    elif sys.platform == "darwin":
        browsers_path = Path.home() / "Library" / "Caches" / "ms-playwright"
    else:  # Linux and other Unix-like OSes
        browsers_path = Path.home() / ".cache" / "ms-playwright"

    # Search for any folder that contains the word 'chromium'
    chromium_folders = list(browsers_path.glob("*chromium*"))

    chromium_installed = bool(chromium_folders)
    if chromium_installed:
        for folder in chromium_folders:
            print(f"Found chromium folder: {folder}")
    else:
        print("No chromium folder found")

    if not chromium_installed:
        print("Browser binaries not found. Installing now...")
        # Run playwright install chromium in subprocess
        import subprocess

        result = subprocess.run(
            ["playwright", "install", "chromium"], capture_output=True, text=True
        )
        print("Installation output:")
        print(result.stdout)
        if result.stderr:
            print("Error output:")
            print(result.stderr)
    else:
        print("Browser binaries are already installed.")

    # Get the browser path from chromium_folders
    chromium_folders = list(browsers_path.glob("*chromium*"))
    browser_path = chromium_folders[0]

    # Find the specific browser executable based on the platform
    if sys.platform == "darwin":
        browser_path = (
            browser_path
            / "chrome-mac"
            / "Chromium.app"
            / "Contents"
            / "MacOS"
            / "Chromium"
        )
    elif sys.platform == "linux":
        browser_path = browser_path / "chrome-linux" / "chrome"
    elif sys.platform == "win32":
        browser_path = browser_path / "chrome-win" / "chrome.exe"

    return browser_path


async def get_browser_and_page(
    playwright, capsolver_api_key: Optional[str] = None
) -> Tuple[Browser, Page]:
    """
    Initialize and return a Playwright browser and page with stealth settings.

    This function sets up a browser with stealth settings to avoid detection,
    and optionally includes a CAPTCHA solver extension.

    Parameters
    ----------
    playwright : Playwright
        The Playwright instance to use for launching the browser.
    capsolver_api_key : Optional[str], optional
        The API key for the CAPTCHA solver service (default is None).

    Returns
    -------
    Tuple[Browser, Page]
        A tuple containing the initialized Browser and Page objects.

    Notes
    -----
    This function uses the playwright_stealth module to apply stealth settings
    and the capsolver_extension_python for CAPTCHA solving capabilities.
    """
    browser_path = _check_for_playwright()

    from playwright_stealth import stealth_async

    # Check if CAPSOLVER_API_KEY exists
    if capsolver_api_key is None:
        capsolver_api_key = os.getenv("CAPSOLVER_API_KEY")

    if capsolver_api_key is None or capsolver_api_key == "":
        print(
            "Warning: No capsolver API key provided. Attempting to launch browser without a captcha solver"
        )

    from capsolver_extension_python import Capsolver

    extension_path = Capsolver(api_key=capsolver_api_key).load(
        with_command_line_option=False
    )
    user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    browser = await playwright.chromium.launch(
        headless=True,
        executable_path=browser_path,
        args=[
            "--disable-extensions-except=" + extension_path,
            "--load-extension=" + extension_path,
            "--user-agent=" + user_agent,
        ],
        proxy=get_proxy(),
    )
    page = await browser.new_page()
    await stealth_async(page)
    return browser, page


async def _extract_plain_text(page: Page) -> str:
    """
    Extract plain text content from a Playwright page.

    This function extracts the text content from the page, removing unwanted elements
    and formatting the text for readability.

    Parameters
    ----------
    page : Page
        The Playwright Page object from which to extract text.

    Returns
    -------
    str
        The extracted and formatted plain text content.

    Notes
    -----
    This function uses BeautifulSoup for HTML parsing and applies custom logic
    to differentiate between inline and block elements for better formatting.
    """
    content = await page.content()
    soup = BeautifulSoup(content, "html.parser")

    # Remove scripts and style elements
    for element in soup(["script", "style"]):
        element.decompose()

    # Define blacklists
    link_blacklist = [
        "unwanted_link_keyword1",
        "unwanted_link_keyword2",
    ]  # Adjust as needed

    # Remove blacklisted links
    for link in soup.find_all("a"):
        href = link.get("href", "").lower()
        text = link.text.lower()
        if any(keyword in href or keyword in text for keyword in link_blacklist):
            link.decompose()

    # Define inline and block elements
    inline_elements: Set[str] = {
        "span",
        "a",
        "button",
        "strong",
        "em",
        "i",
        "b",
        "small",
        "code",
    }
    block_elements: Set[str] = {
        "div",
        "main",
        "section",
        "article",
        "section",
        "p",
        "li",
        "ol",
        "ul",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "blockquote",
    }

    def process_element(element):
        """Recursively process HTML elements to extract formatted text."""
        if isinstance(element, NavigableString):
            return element.strip()

        if element.name in inline_elements:
            return (
                " "
                + " ".join(
                    process_element(child)
                    for child in element.children
                    if child.name != "br"
                ).strip()
                + " "
            )
        elif element.name in block_elements:
            return (
                "\n"
                + "\n".join(
                    process_element(child) for child in element.children
                ).strip()
                + "\n"
            )
        else:
            return " ".join(
                process_element(child) for child in element.children
            ).strip()

    text = process_element(soup.body or soup)  # Start processing from body or root
    text = " ".join(text.split())  # Normalize whitespace
    text = (
        text.replace(" \n ", "\n").replace("\n ", "\n").replace(" \n", "\n").strip()
    )  # Final cleanup

    return text


def _resolve_with_wayback_machine(link: str) -> str:
    """
    Resolve a URL using the Wayback Machine.

    This function attempts to find the most recent archived version of a given URL
    using the Wayback Machine.

    Parameters
    ----------
    link : str
        The URL to resolve.

    Returns
    -------
    str
        The URL of the most recent archived version of the page.

    Notes
    -----
    This function uses the waybackpy library to interact with the Wayback Machine API.
    """
    from waybackpy import Url

    user_agent = "Mozilla/5.0 (Windows NT 5.1; rv:40.0) Gecko/20100101 Firefox/40.0"
    wayback_url = Url(link, user_agent)
    wayback_url.newest()
    url = wayback_url.archive_url
    return url


# List of domains for which we prefer to use Wayback Machine resolution
wayback_resolution_whitelist: List[str] = [
    "nytimes",
    "wsj",
    "nyt",
    "latimes",
    "washingtonpost",
    "bbc",
    "cnn",
    "foxnews",
    "nbcnews",
    "cnbc",
    "reuters",
    "apnews",
    "bloomberg",
    "businessinsider",
    "businesswire",
    "theverge",
]


async def browser_scrape(link: str) -> str:
    """
    Asynchronously scrape a webpage to extract text content.

    This function uses Playwright to navigate to a webpage, render its content,
    and extract the text. It includes fallback mechanisms such as using the
    Wayback Machine for certain domains.

    Parameters
    ----------
    link : str
        The URL of the webpage to scrape.

    Returns
    -------
    str
        The extracted text content from the webpage.

    Notes
    -----
    This function includes error handling and attempts to use the Wayback Machine
    as a fallback for certain whitelisted domains if the initial scrape fails.
    """
    from playwright.async_api import async_playwright

    async with async_playwright() as p:
        try:
            browser, page = await get_browser_and_page(p)
            if any(keyword in link for keyword in wayback_resolution_whitelist):
                new_link = _resolve_with_wayback_machine(link)
                link = new_link if new_link else link

            # Validate the link
            if not link.startswith("http://") and not link.startswith("https://"):
                raise ValueError(f"Invalid link: {link}")
            print(f"Navigating to link: {link}")

            await page.goto(link)
            # Wait for the page to load
            await page.wait_for_load_state("networkidle")
            # Additional wait to handle potential CAPTCHAs
            await asyncio.sleep(2)

            extracted_text = await _extract_plain_text(page)
            return extracted_text
        except Exception as e:
            print(f"Error during scraping: {e}")
            # If we've already used Wayback Machine, don't try again
            if any(keyword in link for keyword in wayback_resolution_whitelist):
                return ""
            # Try to resolve with Wayback Machine
            new_link = _resolve_with_wayback_machine(link)
            if new_link and new_link != link:
                return await browser_scrape(new_link)
            else:
                return ""
        finally:
            await browser.close()
