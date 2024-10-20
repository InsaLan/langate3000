import re
import os
import logging

class VpnRules:
    """Class which manages the VPN rules

    Args:
      logger (logging.Logger): logger instance
      command (str): command to execute (add or del), add by default
    """
    def __init__(self, logger: logging.Logger, command="add": str):
        self.logger = logger
        self.command = command
        if command not in ["add", "del"]:
            raise ValueError("Invalid command")
        self.vpns = VpnRules.get_vpns()
        self.modify_rules()


    def get_vpns() -> list:
        """Get the list of vpns from /etc/hosts

        Returns:
            list: list of vpn names
        """
        vpns = []
        with open("/etc/hosts", "r") as f:
            for line in f:
              if match := re.match(r"(vpn\d+)$", line):
                    vpns.append(match.group())
        return vpns

    def modify_rules(self):
        """Add or remove the VPN rules
        """
        for i, vpn in enumerate(self.vpns):
            try:
              status = os.waitstatus_to_exitcode(os.system(f"ip rule {self.command} fwmark {i + 100} table {vpn}"))
              if status == 0:
                self.logger.info(f"Successfully {self.command} rule for {vpn}")
              else:
                self.logger.error(f"Failed to {self.command} rule for {vpn}")
            except ValueError as e:
                self.logger.error(f"Failed to {self.command} rule for {vpn}: {e}")
