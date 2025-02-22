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

	def get_device_info(self, mac: str):
		"""
		Get device informations.
		
		:param mac: MAC address of the device.
		:return: Dict containing informations about the device, its VLAN.
		"""
		
		try:
			hostname = self.get_hostname(mac)
		except HTTPException:
			hostname = "not_found"
		
		ip = self.arp.get_ip(mac)
		
		switches = self.get_all_switches()
		try:
			switch_ip = self.snmp.get_switch_ip(mac, switches.keys())
		except HTTPException:
			switch_ip = "not_found"
			switches["not_found"] = "not_found"
		
		device_info = {
			"hostname": hostname,
			"ip": ip,
			"mac": mac,
			"vlan": self.get_vlan(ip)[0],
			"switch_name": switches[switch_ip],
			"switch_ip": switch_ip
		}
	
	def get_all_switches(self) -> dict[str, str]:
		"""
		Get all switches.
		
		:return: Dict containing all switch names indexed by IP.
		"""
		
		switches = {}
		
		with open("/hosts", "r") as file:
			lines = file.readlines()
		
		for line in lines:
			if line[0] != "#":
				(ip, name) = line.split(" ")
				if ip.split(".")[3] > 100 and ip.split(".")[3] < 200:
					switches[ip] = name.strip()
	
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
		
		return (vlan, self.variables.vlans[vlan])