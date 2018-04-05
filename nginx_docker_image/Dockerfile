FROM nginx:1.13.8-alpine
RUN apk update \
        && rm /usr/share/nginx/html/index.html \
        && apk add bash

ADD index.html /usr/share/nginx/html/index.html
ADD guacamole-common-js /usr/share/nginx/html/guacamole-common-js
ADD env.sh /usr/share/nginx/html/env.sh
RUN chmod +x /usr/share/nginx/html/env.sh
