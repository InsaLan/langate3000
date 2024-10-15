from fastapi import FastAPI
import logging

# TODO: check nftables access before initializing API

logger = logging.getLogger('uvicorn.error')
# for some reason, default loggers are not working with FastAPI

app = FastAPI()

@app.get("/")
def root():
    return "netcontrol is running"