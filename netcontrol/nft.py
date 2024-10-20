import nftables
import json
import logging
import re

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
        rc, output, error = self.nft.cmd("list ruleset")
        if rc != 0 or (error is not None and error != ""):
            raise NftablesException(rc, error)
        return json.loads(output)["nftables"]

    def _add_vpn(self, mark: int, vpn: str) -> None:
        """Adds a VPN to the nftables rule

        Args:
            mark (int): mark value
            vpn (str): VPN routing table name
        """
        try:
            self._execute_nft_cmd(f"add rule insalan netcontrol-forward fwmark {mark} lookup {vpn}")
        except NftablesException as e:
            self.logger.error(f"Failed to add VPN {vpn} with mark {mark}: {e}")

    def _remove_vpn(self, mark: int, vpn: str) -> None:
        """Removes a VPN from the nftables rule

        Args:
            mark (int): mark value
            vpn (str): VPN routing table name
        """
        try:
            self._execute_nft_cmd(f"delete rule insalan netcontrol-forward fwmark {mark} lookup {vpn}")
        except NftablesException as e:
            self.logger.error(f"Failed to remove VPN {vpn} with mark {mark}: {e}")

    def _parse_etc_hosts(self) -> tuple:
        """Parses /etc/hosts and return all vpn entries

        Returns:
            tuple: n-uple of VPN entries
        """
        with open("/etc/hosts", "r") as f:
            lines = f.readlines()
        vpns = []
        for line in lines:
          if match := re.match(r".+(vpn\d+).+", line):
                vpns.append(match.group())
        return tuple(vpns)

    def initialize_vpn(self) -> None:
        """Initializes the VPN routing tables
        """
        vpns = self._parse_etc_hosts()
        for i, vpn in enumerate(vpns):
            self._add_vpn(100+i, vpn)
        self.logger.info(f"Initialized {len(vpns)} VPN routing tables.")

    def remove_vpn(self) -> None:
        """Removes the VPN routing tables
        """
        vpns = self._parse_etc_hosts()
        for i, vpn in enumerate(vpns):
            self._remove_vpn(100+i, vpn)
        self.logger.info(f"Removed {len(vpns)} VPN routing tables.")

class NftablesException(Exception):
    pass
