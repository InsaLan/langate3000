import logging
from .utilities import to_decimal_mac
from puresnmp import Client, V2C, PyWrapper
from fastapi import HTTPException
import asyncio

class Snmp:
    def __init__(self, logger: logging.Logger, community: str):
        self.logger = logger
        self.v2c = V2C(community)

    async def get_switch(self, mac: str, switches: list[str]):
        """
        Get information about the switch that a machine is connected to.
        
        :param mac: Mac address of the machine to locate.
        :param switches: List of all the switch IPs.
        :return: Tuple of (IP address of the switch the machine is connected to, port on the switch).
        """
        
        dec_mac = to_decimal_mac(mac)

        mac_oid = '1.3.6.1.2.1.17.4.3.1.2' # oid for MAC address table
        
        async def check_switch(switch):
            try:
                client = Client(switch, self.v2c)
                with client.reconfigure(timeout=1.4,retries=1):
                    client = PyWrapper(client)
                    oids = {}
                    async for (oid, port) in client.walk(mac_oid):
                        if port in oids.keys():
                            oids[port].append(oid)
                        else:
                            oids[port] = [oid]
                    for port in oids.keys():
                        if len(oids[port]) == 1 and dec_mac in oids[port][0]:
                            return (switch, port)
            except Exception:
                pass
            return None
        
        tasks = [check_switch(switch) for switch in switches]
        results = await asyncio.gather(*tasks)

        for result in results:
            if result:
                return result
    
        self.logger.error(f"SNMP : Could not find switch for device {mac}")
        raise HTTPException(status_code=404, detail="Switch not found")
