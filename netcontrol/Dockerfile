FROM python:3.12-alpine3.19

WORKDIR /nctl

RUN apk add --no-cache nftables git \
	&& pip install 'git+https://git.netfilter.org/nftables@v1.1.0#egg=nftables&subdirectory=py' \
	&& apk del git

COPY requirements.txt /nctl/

RUN pip install -r /nctl/requirements.txt

COPY . /nctl

CMD ["fastapi", "run", "main.py", "--port", "6784"]