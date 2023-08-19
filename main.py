import json
from typing import Union

from fastapi import FastAPI
from fastapi.responses import Response

import browser

app = FastAPI(
    title="Browserless",
    description=(
        "Browserless is a web scraping API that allows you to "
        "scrape any website without getting blocked."
    ),
    version="0.0.1",
    docs_url="/",
)


@app.get("/q/{query}")
async def search(query: str):
    urls = [x["href"] for x in await browser.search(query)]
    contents = await browser.scrape(urls)
    return Response(
        # merge
        content=json.dumps(
            [
                {
                    "url": url,
                    "content": content["content"],
                    "time": content["time"],
                }
                for url, content in zip(urls, contents)
            ],
            indent=2,
        ),
    )
