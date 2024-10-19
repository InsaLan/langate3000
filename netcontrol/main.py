from fastapi import FastAPI
import logging
from .nft import Nft
from .arp import Arp

logger = logging.getLogger('uvicorn.error')
# for some reason, default loggers are not working with FastAPI

logger.info("Checking that nftables is working...")
nft = Nft(logger)
arp = Arp(logger)
nft.check_nftables()

app = FastAPI()

@app.get("/")
def root():
    return "netcontrol is running"

@app.get("/get_mac/{ip_address}")
def get_mac(ip: str):
    return arp.get_mac(ip)

@app.get("/get_ip/{mac_address}")
def get_ip(mac: str):
    return arp.get_ip(mac)