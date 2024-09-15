from apify_client import ApifyClient
import os

from dotenv import load_dotenv

load_dotenv()
# Initialize the ApifyClient with your Apify API token
client = ApifyClient(os.environ["APIFY_API_KEY"])


def crawl_webpage_and_linked_pages_into_md(url: str):
    """Calls the Apify API to crawl a given link and return the processed webpages in markdown string format"""
    md_pages = []
    # Prepare the Actor input
    run_input = {
        "startUrls": [{"url": url}],
        "crawlerType": "playwright:adaptive",
        "includeUrlGlobs": [],
        "excludeUrlGlobs": [],
        "initialCookies": [],
        "proxyConfiguration": {"useApifyProxy": True},
        "removeElementsCssSelector": """nav, footer, script, style, noscript, svg,
    [role=\"alert\"],
    [role=\"banner\"],
    [role=\"dialog\"],
    [role=\"alertdialog\"],
    [role=\"region\"][aria-label*=\"skip\" i],
    [aria-modal=\"true\"]""",
        "clickElementsCssSelector": '[aria-expanded="false"]',
    }

    # Run the Actor and wait for it to finish
    run = client.actor("apify/website-content-crawler").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    print(
        "💾 Check your data here: https://console.apify.com/storage/datasets/"
        + run["defaultDatasetId"]
    )
    for item in client.dataset(run["defaultDatasetId"]).iterate_items():
        md_pages.append({"text": item["markdown"], "file_url": item["url"]})
    return md_pages
