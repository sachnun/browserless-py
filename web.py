from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from browser import browser_search

import typing
import logging

logging.basicConfig(level=logging.DEBUG)

app = FastAPI(
    title="Browser Search",
    description="Search the web and parse articles",
    version="0.1",
    docs_url="/",
)


# ?q=python
@app.get("/search/")
def read_item(
    q: str = Query(None, description="Search query", example="python"),
    # limit min 1-10
    limit: typing.Optional[int] = Query(
        10, ge=1, le=10, description="Number of results"
    ),
):
    results = browser_search(q, limit)
    return JSONResponse(content=results)


# 500 internal server error
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )
