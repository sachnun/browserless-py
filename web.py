from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from browser import browser_search

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
def read_item(q: str = Query(None, description="Search query", example="python")):
    results = browser_search(q)
    return JSONResponse(content=results)


# 500 internal server error
@app.exception_handler(Exception)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": str(exc)},
    )
