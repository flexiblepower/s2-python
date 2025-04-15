try:
    from fastapi import FastAPI
except ImportError as exc:
    raise ImportError(
        "The 'fastapi' package is required. Run 'pip install s2-python[fastapi]' to use this feature."
    ) from exc


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
