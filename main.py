from fastapi import FastAPI
app = FastAPI()


@app.get("/")
async def read_root():
    """
    Descriptions written in markdown.
    """

    return {"items": ["one", "two", "three"]}

