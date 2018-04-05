FROM python:3.4-alpine

RUN apk update \
	&& apk add bash \
        && apk add git \
        && apk add --no-cache openssl-dev libffi-dev musl-dev make gcc \
        && apk add py-mysqldb \
        && apk add mariadb-dev \
        && mkdir medusa_keys \
	&& mkdir -p home/opc/.oci \
        && git clone https://github.com/bpeters-cmu/Project-Medusa-r-.git \
	&& apk add --no-cache openssl  

WORKDIR /Project-Medusa-r-
RUN pip install -r requirements.txt

ADD config.py /Project-Medusa-r-/
EXPOSE 8000
RUN openssl req -new -newkey rsa:4096 -days 365 -nodes -x509 \
    -subj "/C=US/ST=Texas/L=Austin/O=Oracle/CN=Medusa" \
    -keyout key.pem  -out cert.pem
