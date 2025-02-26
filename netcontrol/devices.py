import logging
from .variables import Variables
from .arp import Arp
from .snmp import Snmp
from fastapi import HTTPException

class Devices:
    def __init__(self, logger: logging.Logger, variables: Variables, snmp: Snmp, arp: Arp):
        self.logger = logger
        self.variables = variables
        self.snmp = snmp
        self.arp = arp
        self.switches = {}

    async def get_device_info(self, mac: str):
        """
        Get device informations.
        
        :param mac: MAC address of the device.
        :return: Dict containing informations about the device, its VLAN.
        """
        
        try:
            hostname = self.get_hostname(mac)
        except HTTPException:
            hostname = "not_found"
        
        ip = self.arp.get_ip(mac)["ip"]
        vlan = self.get_vlan(ip)
        
        switches = self.get_all_switches()
        try:
            switch_ip, switch_port = await self.snmp.get_switch(mac, switches.keys())
        except HTTPException:
            switch_ip = "not_found"
            switches["not_found"] = "not_found"
            switch_port = -1
        
        self.logger.info(f"Fetched information for device {mac} (ip: {ip})")
        
        return {
            "hostname": hostname,
            "ip": ip,
            "vlan_number": vlan[0],
            "vlan_name": vlan[1],
            "switch_name": switches[switch_ip],
            "switch_ip": switch_ip,
            "switch_port": switch_port
        }
    
    def get_all_switches(self) -> dict[str, str]:
        """
        Get all switches.
        
        :return: Dict containing all switch names indexed by IP.
        """
        
        if self.switches == {}:
            with open("/hosts", "r") as file:
                lines = file.readlines()
            
            for line in lines:
                if line[0] != "#":
                    if len(line.split()) > 1:
                        ip = line.split()[0]
                        name = line.split()[1]
                        if len(ip.split(".")) == 4:
                            if int(ip.split(".")[0]) == 172 and int(ip.split(".")[3]) > 20 and int(ip.split(".")[3]) < 200:
                                self.switches[ip] = name.strip()
        
        return self.switches
    
    def get_hostname(self, mac: str) -> str:
        """
        Get hostname of a device.
        
        :param mac: MAC address of the device.
        :return: Hostname of the device.
        """
        
        with open("/dnsmasq.leases") as file:
            lines = file.readlines()
        
        for line in lines:
            parts = line.split()
            if parts[1] == mac:
                return parts[3]
        
        self.logger.error(f"Could not find device {mac} in dnsmasq.leases")
        raise HTTPException(status_code=404, detail="Device not found")
    
    def get_vlan(self, ip: str) -> tuple[int, str]:
        """
        Get VLAN of an IP.
        
        :param ip: IP address of the device.
        :return: VLAN name.
        """
        
        ip_parts = ip.split(".")
        try:
            if int(ip_parts[1]) == 16 and int(ip_parts[2]) == 1:
                vlan = 1
            else :
                vlan:int = 100 + (int(ip_parts[1])-17)*10 + int(ip_parts[2])
                if vlan < 100 or vlan > 199:
                    vlan = 0
        except:
            vlan = 0
        
        return (vlan, self.variables.vlans()[vlan])

class MockedDevices(Devices):
    def __init__(self, logger):
        self.logger = logger
    
    async def get_device_info(self, mac):
        self.logger.info(f"Fetched information for device {mac} (ip: 127.0.0.1)")
        
        return {
            "hostname": "computer",
            "ip": "127.0.0.1",
            "vlan_number": 1,
            "vlan_name": "v001-management",
            "switch_name": "Hydrogen-1",
            "switch_ip": "172.16.1.101",
            "switch_port": "0"
        }
