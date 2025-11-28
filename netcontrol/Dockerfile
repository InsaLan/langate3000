FROM debian:bookworm-slim

WORKDIR /nctl

RUN apt-get update && apt-get install -y --no-install-recommends \
		python3-pip \
		python3-setuptools \
		nftables \
		python3-nftables

COPY requirements.txt /nctl/

RUN python3 -m pip install --no-cache-dir --break-system-packages -r /nctl/requirements.txt

COPY . /nctl

CMD ["fastapi", "run", "main.py", "--port", "6784"]