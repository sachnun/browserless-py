import asyncio
import json
import random
import time
from itertools import islice

import html2markdown
import httpx
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS


# duckduckgo_search
async def search(query, max_results=10):
    with DDGS() as ddgs:
        ddgs_gen = ddgs.text(query, backend="lite")
        return [r for r in islice(ddgs_gen, max_results)]


# user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/20A5312g [FBAN/FBIOS;FBDV/iPhone13,1;FBMD/iPhone;FBSN/iOS;FBSV/16.0;FBSS/3;FBID/phone;FBLC/cs_CZ;FBOP/5]"
ua_gpt = "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko; compatible; GPTBot/1.0; +https://openai.com/gptbot)"


# run all requests concurrently using httpx
async def scrape(urls: list[str]):
    async with httpx.AsyncClient(
        headers={
            "User-Agent": ua_gpt,
            "X-Forwarded-For": ".".join(
                [str(random.randint(0, 255)) for _ in range(4)]
            ),
        }
    ) as client:

        async def get_one(url):
            start = time.time()
            try:
                r = await client.get(url, timeout=5)
                r.raise_for_status()
                html = r.text
            except:
                html = ""
            finally:
                print(f"GET {url}")

            return {
                "content": extract_text(html),
                "time": time.time() - start,
            }

        tasks = [get_one(url) for url in urls]
        return await asyncio.gather(*tasks)


import re


# extract text from html
def extract_text(html):
    # make split 3000 chars (must split end space)
    def split(text, size=3000):
        return re.findall(r".{1,%d}(?:\s|$)" % size, text, re.DOTALL)

    soup = BeautifulSoup(html, "html.parser")
    return split(html2markdown.convert(soup.text))


# test
if __name__ == "__main__":
    urls = [x["href"] for x in asyncio.run(search("indinesia"))]
    print(urls)

    # only show length of response
    contents = asyncio.run(scrape(urls))

    # merge results
    marge = [
        {
            "url": url,
            "content": len(content["content"]),
            "time": content["time"],
        }
        for url, content in zip(urls, contents)
    ]
    print(json.dumps(marge, indent=4))
