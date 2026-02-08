from fastapi import FastAPI
import os

app = FastAPI()

VERSION = os.getenv("VERSION", "dev")
ENV = os.getenv("ENVIRONMENT", "dev")


@app.get("/health")
def health():
    return {"status": "OK"}


@app.get("/version")
def version():
    return {"version": VERSION}


@app.get("/env")
def environment():
    return {"environment": ENV}
