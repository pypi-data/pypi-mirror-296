# Utils
import os
import time


# Webscraping
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from firecrawl import FirecrawlApp


def get_webpage_content(url: str):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string if soup.title else ""
        text_content = " ".join(soup.stripped_strings)
        return True, f"{title}\n{text_content}"
    except requests.exceptions.RequestException as e:
        return False, e


def scrape_website_firecrawl(url):
    app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_API_KEY"))
    scrape_result = app.scrape_url(url=url, params={"formats": ["markdown"]})
    return scrape_result


def web_search_ddg(search_term: str):
    results = DDGS().text(search_term, max_results=5)
    return results
