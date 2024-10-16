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

@app.post("/connect_user/")
def connect_user(mac: str, mark: int, name: str):
    return nft.connect_user(mac, mark, name)

@app.delete("/disconnect_user/{mac}")
def delete_user(mac: str):
    return nft.delete_user(mac)

@app.put("/set_mark/")
def set_mark(mac: str, mark: int):
    return nft.set_mark(mac, mark)