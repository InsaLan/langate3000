import requests
import subprocess
import logging

GET_REQUESTS = ["get_mac", "get_ip"]
POST_REQUESTS = ["connect_user"]
DELETE_REQUESTS = ["disconnect_user"]
PUT_REQUESTS = ["set_mark"]

class RequestError(Exception):
    """
    Exception raised when a request to the netcontrol API fails.
    """
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

class Netcontrol:
    """
    Class which interacts with the netcontrol API.
    """
    def __init__(self):
        """
        Initialize HOST_IP to the docker's default route and check the connection with the netcontrol API.
        """
        self.HOST_IP = subprocess.run(["/sbin/ip", "route"], capture_output=True).stdout.decode("utf-8").split()[2]
        self.logger = logging.getLogger(__name__)

        try:
            self.logger.info("Checking connection with the netcontrol API...")
            if requests.get(f"http://{self.HOST_IP}:6784/") != "netcontrol is running":
                raise RequestError("Netcontrol is not running.")
        except requests.exceptions.ConnectionError:
            self.logger.info("Could not connect to the netcontrol API.")
        except RequestError as e:
            self.logger.info(e.message)

    def request(self, endpoint='', args={}):
        """
        Make a given request to the netcontrol API.
        """
        # Construct the data to be sent in the request
        if len(args) == 1:
            data = '/'+args[0]
        elif len(args) > 1:
            data = '?' + "&".join([f"{key}={value}" for key, value in args.items()])
        else:
            data = ''

        # Make the request
        try:
            # Check the type of request
            if endpoint in GET_REQUESTS:
                response = requests.get(f"http://{self.HOST_IP}:6784/{endpoint}{data}")
            elif endpoint in POST_REQUESTS:
                response = requests.post(f"http://{self.HOST_IP}:6784/{endpoint}{data}")
            elif endpoint in DELETE_REQUESTS:
                response = requests.delete(f"http://{self.HOST_IP}:6784/{endpoint}{data}")
            elif endpoint in PUT_REQUESTS:
                response = requests.put(f"http://{self.HOST_IP}:6784/{endpoint}{data}")
            
            # Check for errors in the response
            if response.json()["error"]:
                raise RequestError(response.json()["error"])
            return response.json()
        
        # Handle exceptions
        except requests.exceptions.ConnectionError:
            self.logger.info("Could not connect to the netcontrol API.")
        except RequestError as e:
            self.logger.info(e.message)

    def check_api(self):
        """
        Check if the netcontrol API is running.
        """
        self.logger.info("Checking connection with the netcontrol API...")
        return self.request()

    def get_mac(self, ip: str):
        """
        Get the MAC address of the device with the given IP address.
        """
        self.logger.info(f"Getting MAC address of {ip}...")
        return self.request("get_mac", {"ip": ip})["mac"]
    
    def get_ip(self, mac: str):
        """
        Get the IP address of the device with the given MAC address.
        """
        self.logger.info(f"Getting IP address of {mac}...")
        return self.request("get_ip", {"mac": mac})["ip"]
    
    def connect_user(self, mac: str, mark: int, name: str):
        """
        Connect the user with the given MAC address.
        """
        self.logger.info(f"Connecting user with MAC address {mac} ({name})...")
        return self.request("connect_user", {"mac": mac, "mark": mark, "name": name})
    
    def disconnect_user(self, mac: str):
        """
        Disconnect the user with the given MAC address.
        """
        self.logger.info(f"Disconnecting user with MAC address {mac}...")
        return self.request("disconnect_user", {"mac": mac})
    
    def set_mark(self, mac: str, mark: int):
        """
        Set the mark of the user with the given MAC address.
        """
        self.logger.info(f"Setting mark of user with MAC address {mac} to {mark}...")
        return self.request("set_mark", {"mac": mac, "mark": mark})
    
