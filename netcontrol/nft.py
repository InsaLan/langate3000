import nftables
import json
import logging
from fastapi import HTTPException

class Nft:
    """Class which interacts with the nftables backend
    """
    def __init__(self, logger: logging.Logger):
        self.logger = logger
        self.nft = nftables.Nftables()
        self.nft.set_json_output(True)

    def check_nftables(self):
        data = self._execute_nft_cmd("list ruleset")
        metainfo = data[0]["metainfo"]
        self.logger.info(f"Found running nftables version {metainfo['version']} with {len(data)} ruleset entries.")
    
    def _execute_nft_cmd(self, cmd: str) -> dict:
        """Executes an nft command, handles the exception properly and returns an object

        Args:
            cmd (str): string representation of the command

        Raises:
            NftablesException: if the command returned an exception

        Returns:
            dict: parsed JSON output
        """
        output: str
        rc, output, error = self.nft.cmd(cmd)
        if rc != 0 or (error is not None and error != ""):
            raise NftablesException(rc, error)
        return json.loads(output)["nftables"]
    
    def setup_portail(self):
        """Sets up the necessary nftables rules that block network access to unauthenticated devices, and marks packets based on the map
        """
        
        # Set up table and map
        self._execute_nft_cmd("add table ip insalan")
        self._execute_nft_cmd("add map insalan netcontrol-mac2mark { type ether_addr : mark; }")
        
        # Marks packets from authenticated users using the map
        self._execute_nft_cmd("add chain insalan netcontrol-filter { type filter hook prerouting priority 0; }")
        self._execute_nft_cmd("add rule insalan netcontrol-filter ip daddr != 172.16.1.0/24 ether saddr @netcontrol-mac2mark meta mark set ether saddr map @netcontrol-mac2mark")
        
        # Allow traffic to port 80 from unauthenticated devices and redirect it to the network head, to allow access to the langate webpage
        self._execute_nft_cmd("add chain insalan netcontrol-nat { type nat hook prerouting priority 0; }")
        self._execute_nft_cmd("add rule insalan netcontrol-nat ip daddr != 172.16.1.0/24 ether saddr != @netcontrol-mac2mark tcp dport 80 redirect to :80")
        
        # Block other traffic from users that are not authenticated
        self._execute_nft_cmd("add chain insalan netcontrol-forward { type filter hook forward priority 0; }")
        self._execute_nft_cmd("add rule insalan netcontrol-forward ip daddr != 172.16.1.1 ether saddr != @netcontrol-mac2mark reject")
        
        self.logger.info("Gate nftables set up")
        
    def remove_portail(self):
        """Removes netcontrol-related chains and maps from insalan table
        """
        self._execute_nft_cmd("delete chain insalan netcontrol-filter")
        self._execute_nft_cmd("delete chain insalan netcontrol-nat")
        self._execute_nft_cmd("delete chain insalan netcontrol-forward")
        self._execute_nft_cmd("delete map insalan netcontrol-mac2mark")
        
        self.logger.info("Gate nftables removed")

    def set_mark(self, mac: str, mark: int):
        """Changes mark of the given MAC address
        
        Args:
            mac (str): MAC address
            mark (int): mark to set
        """
        
        self.delete_user(mac)
        return self.connect_user(mac, mark)

    def connect_user(self, mac: str, mark: int, name: str):
        """Connects given device with given mark
        
        Args:
            mac (str): MAC address
        """
        
        if name == None:
            name = "previously_connected_device"
        
        mac = mac.lower()
        try:
            self._execute_nft_cmd("add element insalan netcontrol-mac2mark { "+mac+" : "+mark+" }")
        except NftablesException:
            self.logger.error("Tried to add device {mac} (name: {name}), unexpected nftables error occurred")
            raise HTTPException(status_code=404, detail="Unexpected nftables error occurred")
        
        self.logger.info(f"Device {mac} (name: {name}) connected with mark {mark}")
        return {"success": "yeah"}

    def delete_user(self, mac: str) -> None:
        """Disconnects given device
        
        Args:
            mac (str): MAC address
        """
        
        mac = mac.lower()
        try:
            self._execute_nft_cmd("delete element insalan netcontrol-mac2mark { "+mac+" : * }")
        except NftablesException:
            self.logger.error(f"Tried to delete device {mac} which was not previously connected")
            raise HTTPException(status_code=404, detail="Device was not previously connected")
        
        self.logger.info(f"Device {mac} disconnected")
        return {"success": "yeah"}

class NftablesException(Exception):
    pass