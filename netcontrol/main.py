from fastapi import FastAPI
from contextlib import asynccontextmanager
import os
import logging
from .variables import Variables
from .nft import Nft, MockedNft
from .arp import Arp, MockedArp
from .snmp import Snmp
from .devices import Devices, MockedDevices

mock = os.getenv("MOCK_NETWORK", "0") == "1"
snmp_community = os.getenv("SNMP_COMMUNITY", "")

logger = logging.getLogger('uvicorn.error')
# for some reason, default loggers are not working with FastAPI

variables = Variables()
snmp= Snmp(logger, snmp_community)
if mock:
    logger.warning("MOCK_NETWORK is set to 1, Nftables rules will not be applied.")
    nft = MockedNft(logger)
    arp = MockedArp(logger)
    devices = MockedDevices(logger)
else:
    nft = Nft(logger, variables)
    arp = Arp(logger)
    devices = Devices(logger, variables, snmp, arp)

logger.info("Checking that nftables is working...")
nft.check_nftables()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Function that "wraps" around the FastAPI app's lifespan :
    The part before the yield is executed before the app starts;
    The part after the yield is executed after the app stops.
    """
    
    nft.setup_portail()
    
    yield
    
    nft.remove_portail()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return "netcontrol is running"
 
@app.post("/connect_user")
def connect_user(mac: str, mark: int, bypass: bool, name: str) -> None:
    nft.connect_user(mac, mark, bypass, name)

@app.delete("/disconnect_user")
def delete_user(mac: str) -> None:
    nft.delete_user(mac)

@app.put("/set_mark")
def set_mark(mac: str, mark: int, bypass: bool) -> None:
    nft.set_mark(mac, mark, bypass)

@app.get("/get_mac")
def get_mac(ip: str):
    return arp.get_mac(ip)

@app.get("/get_ip")
def get_ip(mac: str):
    return arp.get_ip(mac)

@app.get("/get_device_info")
def get_device_info(mac:str):
    return devices.get_device_info(mac)