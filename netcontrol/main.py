from fastapi import FastAPI
import logging
from .nft import Nft

logger = logging.getLogger('uvicorn.error')
# for some reason, default loggers are not working with FastAPI

logger.info("Checking that nftables is working...")
nft = Nft(logger)
nft.check_nftables()

app = FastAPI()

@app.get("/")
def root():
    return "netcontrol is running"