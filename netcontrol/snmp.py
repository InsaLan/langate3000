import logging
from .utilities import to_decimal_mac
from puresnmp import Client, V2C, PyWrapper
from fastapi import HTTPException
import asyncio

TIMEOUT = 2.5
RETRIES = 2

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
                with client.reconfigure(timeout=TIMEOUT,retries=RETRIES):
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
        
        tasks = [asyncio.create_task(check_switch(switch)) for switch in switches]

        while tasks:
            done, pending = await asyncio.wait(
                tasks,
                return_when=asyncio.FIRST_COMPLETED
            )

            for task in done:
                result = task.result()
                if result is not None:
                    for pending_task in pending:
                        pending_task.cancel()
                    return result

            tasks = list(pending)
    
        self.logger.error(f"SNMP : Could not find switch for device {mac}")
        raise HTTPException(status_code=404, detail="Switch not found")
