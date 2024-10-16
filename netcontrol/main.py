from fastapi import FastAPI
import logging
import re

# TODO: check nftables access before initializing API

logger = logging.getLogger('uvicorn.error')
# for some reason, default loggers are not working with FastAPI



def verify_ip(ip: str) -> bool:
    """
    Verify if ip address is correctly formed.

    :param ip: Ip address to verify.
    :return: True is correctly formed, False if not.
    """
    return bool(re.match(r'^([0-9]{1,3}\.){3}[0-9]{1,3}$', ip)) # Check if ip is in the form of xxx.xxx.xxx.xxx using a regex



app = FastAPI()

@app.get("/")
def root():
    return "netcontrol is running"

@app.get("/get_mac/{ip_address}")
def get_mac(ip: str):
    """
    Get the mac address associated with a given ip address.

    :param ip: Ip address of the machine.
    :return: Mac address of the machine.
    """
    logger.info("Querying MAC for IP %s", ip)
    if not verify_ip(ip):
        return {"error": "Invalid IP address"}
    f = open('/proc/net/arp', 'r') # Open arp table
    lines = f.readlines()[1:]
    for line in lines:
        if line.startswith(ip + " "):
            mac = line[41:].split(" ")[0] # 41 is the position of the MAC address in the line
            logger.info("Found MAC %s for IP %s", mac, ip)
            return { "mac" : mac}
    return {"error": "MAC not found"}

@app.post("/connect_user/")
def connect_user(mac: str = "", mark: int = 0, name: str = ""):
    return {"error": "Not implemented"}

@app.delete("/disconnect_user/{mac}")
def delete_user(mac: str):
    return {"error": "Not implemented"}

@app.put("/set_mark/")
def set_mark(mac: str, mark: int):
    return {"error": "Not implemented"}