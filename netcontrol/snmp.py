import logging
import pysnmp.hlapi.v3arch.asyncio
import pysnmp.smi.rfc1902
from fastapi import HTTPException
import asyncio

class Snmp:
    def __init__(self, logger: logging.Logger, community: str):
        self.logger = logger
        
        self.snmp_engine = pysnmp.hlapi.v3arch.asyncio.SnmpEngine()
        self.community_data = pysnmp.hlapi.v3arch.asyncio.CommunityData(community, mpModel=1)
        self.context_data = pysnmp.hlapi.v3arch.asyncio.ContextData()
    
    async def get_switch(self, mac: str, switches: list[str]):
        """
        Get information about the switch that a machine is connected to.
        
        :param mac: Mac address of the machine to locate.
        :param switches: List of all the switch IPs.
        :return: IP address of the switch the machine is connected to.
        """
        
        mac = mac.lower()
        
        oid = '1.3.6.1.2.1.17.4.3.1.2' # oid for MAC address table
        object_type = pysnmp.smi.rfc1902.ObjectType(pysnmp.smi.rfc1902.ObjectIdentity(oid))
        
        async def check_switch(switch):
            async for errorIndication, errorStatus, errorIndex, varBinds in pysnmp.hlapi.v3arch.asyncio.nextCmd(
                self.snmp_engine,
                self.community_data,
                pysnmp.hlapi.v3arch.asyncio.UdpTransportTarget((switch, 161)),
                self.context_data,
                object_type,
                lexicographicMode=False,
            ):
                if not errorIndication:
                    for var in varBinds:
                        if mac in var.lower():
                            return switch
                return None
        
        tasks = [check_switch(switch) for switch in switches]
        results = await asyncio.gather(*tasks)
        
        for result in results:
            if result:
                return result
    
        self.logger.error(f"SNMP : Could not find switch for device {mac}")
        raise HTTPException(status_code=404, detail="Switch not found")