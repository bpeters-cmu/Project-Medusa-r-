FROM node:8-alpine
RUN apk update \
        && apk add bash \
        && apk add git \
        && apk add --no-cache openssl-dev libffi-dev musl-dev python3-dev make gcc \
        && git clone https://github.com/bpeters-cmu/SSH2-Medusa.git \
        && apk add python3 \
        && pip3 install --upgrade pip setuptools \
        && pip3 install -U wheel

RUN pip3 install simple-crypt
WORKDIR /SSH2-Medusa/
RUN npm install system-sleep \
	&& npm install \
        && mkdir medusa_keys
EXPOSE 2222

