import logging
from pysnmp.hlapi import *
from fastapi import HTTPException

class Snmp:
    def __init__(self, logger: logging.Logger, community: str):
        self.logger = logger
        self.community = community
    
    def get_switch(self, mac: str, switches: list[str]):
        """
        Get information about the switch that a machine is connected to.
        
        :param mac: Mac address of the machine to locate.
        :param switches:
        """
        
        oid = '1.3.6.1.2.1.17.4.3.1.2' # oid for MAC address table

        for switch in switches:
            for errorIndication, errorStatus, errorIndex, varBinds in nextCmd(
                SnmpEngine(),
                CommunityData(self.community, mpModel=1),
                UdpTransportTarget((switch, 161)),
                ContextData(),
                ObjectType(ObjectIdentity(oid)),
                lexicographicMode=False,
            ):
                if not errorIndication:
                    for var in varBinds:
                        if mac in var:
                            result = switch
                            break
                    if result:
                        break
            
        if result:
            return result
        else:
            self.logger.error(f"SNMP : Could not find switch for device {mac}")
            raise HTTPException(status_code=404, detail="Switch not found")