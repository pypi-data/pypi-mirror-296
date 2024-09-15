import os
import time
from apify_client import ApifyClient


def get_google_reviews_apify(placeId, reviews_start_date=None, retries=3):
    apify_client = ApifyClient(os.environ["APIFY_TOKEN"])

    false = False
    true = True
    run_input = {
        "deeperCityScrape": false,
        "includeWebResults": false,
        "language": "en",
        "maxImages": 0,
        "maxReviews": 2000,
        "oneReviewPerRow": true,
        "onlyDataFromSearchPage": false,
        "scrapeResponseFromOwnerText": true,
        "scrapeReviewId": true,
        "scrapeReviewUrl": true,
        "scrapeReviewerId": true,
        "scrapeReviewerName": true,
        "scrapeReviewerUrl": true,
        "searchStringsArray": ["place_id:" + placeId],
    }
    if reviews_start_date:
        run_input["reviewsStartDate"] = reviews_start_date
    google_reviews = []
    try:
        run = apify_client.actor("compass/crawler-google-places").call(
            run_input=run_input
        )
        for item in apify_client.dataset(run["defaultDatasetId"]).iterate_items():
            google_reviews.append(item)
    except Exception as e:
        time.sleep(600)
        retries -= 1
        if retries > 0:
            google_reviews = get_google_reviews_apify(placeId, reviews_start_date)
        else:
            print("ERRORs on apify:", e)
            return []
    return google_reviews
