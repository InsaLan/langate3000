import logging

class Arp:
    """
    Class which interacts with the ARP table
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def get_mac(self, ip: str):
        """
        Get the mac address associated with a given ip address.

        :param ip: Ip address of the machine.
        :return: Mac address of the machine.
        """
        self.logger.info("Querying MAC for IP %s", ip)
        f = open('/proc/net/arp', 'r') # Open arp table
        lines = f.readlines()[1:]
        for line in lines:
            if line.startswith(ip + " "):
                mac = line[41:].split(" ")[0] # 41 is the position of the MAC address in the line
                self.logger.info("Found MAC %s for IP %s", mac, ip)
                return { "mac" : mac}
        return {"error": "MAC not found"}
    
    def get_ip(self, mac: str):
        """
        Get the mac address associated with a given ip address.

        :param ip: Ip address of the machine.
        :return: Mac address of the machine.
        """
        self.logger.info("Querying IP for MAC %s", mac)
        f = open('/proc/net/arp', 'r') # Open arp table
        lines = f.readlines()[1:]
        for line in lines:
            if line[41:].split(" ")[0] == mac:
                ip = line.split(" ")[0] # 41 is the position of the MAC address in the line
                self.logger.info("Found IP %s for MAC %s", ip, mac)
                return { "ip" : ip}
        return {"error": "IP not found"}