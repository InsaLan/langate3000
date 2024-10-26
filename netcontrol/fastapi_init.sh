#! /bin/sh

# Get the IP address of the docker bridge
IP="$(ip addr show docker0 | awk '/inet / {print $2}' | cut -d'/' -f1)"
# Run the FastAPI server
fastapi run main.py --host $IP --port 6784