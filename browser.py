from googlesearch import search
import article_parser
import json
import threading

import warnings
from urllib3.exceptions import InsecureRequestWarning

# Suppress only the single warning from urllib3
warnings.filterwarnings("ignore", category=InsecureRequestWarning)


def parse_article(result, all_results):
    try:
        _, content = article_parser.parse(
            url=result.url, output="markdown", verify=False
        )
    except Exception:
        _, content = None, None

    all_results.append(
        {
            "url": result.url,
            "title": result.title,
            "content": content,
        }
    )


def browser_search(query):
    google = search(query, num_results=10, advanced=True)
    all_results = []

    threads = []
    for result in google:
        t = threading.Thread(target=parse_article, args=(result, all_results))
        t.start()
        threads.append(t)

    # Wait for all threads to finish
    for t in threads:
        t.join()

    return all_results


if __name__ == "__main__":
    while True:
        query = input("Search: ")
        results = browser_search(query)
        print(json.dumps(results, indent=4))
