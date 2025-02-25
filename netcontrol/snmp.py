import logging
from .utilities import to_decimal_mac
import pysnmp.hlapi.v3arch.asyncio
import pysnmp.smi.rfc1902
from fastapi import HTTPException
import asyncio

class Snmp:
    def __init__(self, logger: logging.Logger, community: str):
        self.logger = logger
        self.community = community

    async def get_switch(self, mac: str, switches: list[str]):
        """
        Get information about the switch that a machine is connected to.
        
        :param mac: Mac address of the machine to locate.
        :param switches: List of all the switch IPs.
        :return: Tuple of (IP address of the switch the machine is connected to, port on the switch).
        """
        
        dec_mac = to_decimal_mac(mac)
        
        snmp_engine = pysnmp.hlapi.v3arch.asyncio.SnmpEngine()
        community_data = pysnmp.hlapi.v3arch.asyncio.CommunityData(self.community, mpModel=1)
        context_data = pysnmp.hlapi.v3arch.asyncio.ContextData()

        oid = '1.3.6.1.2.1.17.4.3.1.2' # oid for MAC address table
        object_type = pysnmp.smi.rfc1902.ObjectType(pysnmp.smi.rfc1902.ObjectIdentity(oid))
        
        async def check_switch(switch):
            for errorIndication, errorStatus, errorIndex, varBinds in await pysnmp.hlapi.v3arch.asyncio.next_cmd(
                snmp_engine,
                community_data,
                await pysnmp.hlapi.v3arch.asyncio.UdpTransportTarget.create((switch, 161)),
                context_data,
                object_type,
            ):
                if errorIndication or errorStatus:
                    break
                else:
                    for var in varBinds:
                        oid, port = var
                        if dec_mac in oid:
                            return (switch, port)
            return None
        
        tasks = [check_switch(switch) for switch in switches]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:
                return result
    
        self.logger.error(f"SNMP : Could not find switch for device {mac}")
        raise HTTPException(status_code=404, detail="Switch not found")
