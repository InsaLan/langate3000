import subprocess

def get_ip():
    """
    Function that returns the IP of the docker bridge.
    """
    return subprocess.run(["ip", "-br", "address", "show", "dev", "docker0"], capture_output=True).stdout.decode().split()[2][:-3]

subprocess.run(["fastapi", "run", "main.py", "--host", get_ip(), "--port", "6784"])