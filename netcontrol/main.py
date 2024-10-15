from fastapi import FastAPI
import logging

from os import getenv

# Import Docker env vars
MARK = [int(x.strip()) for x in getenv("MARK", "[100, 1]").strip('[]').split(',')]
SOCKET_FILE = getenv("SOCKET_FILE", "/var/run/langate3000-netcontrol.sock")

# TODO: check nftables access before initializing API

logger = logging.getLogger('uvicorn.error')
# for some reason, default loggers are not working with FastAPI

app = FastAPI()

@app.get("/")
def root():
    return "netcontrol is running"