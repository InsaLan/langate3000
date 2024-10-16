import nftables
import json
import logging

class Nft:
    """
    Class which interacts with the nftables backend
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
        """
        Executes an nft command, handles the exception properly and returns an object

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
    
    def connect_user(mac: str = "", mark: int = 0, name: str = ""):
        return {"error": "Not implemented"}
    
    def delete_user(mac: str):
        return {"error": "Not implemented"}

    def set_mark(mac: str, mark: int):
        return {"error": "Not implemented"}

class NftablesException(Exception):
    pass