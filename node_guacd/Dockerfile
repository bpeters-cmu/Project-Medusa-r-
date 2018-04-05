FROM glyptodon/guacd
RUN yum install -y curl        
RUN yum install -y gcc-c++ make 
RUN curl -y -sL https://rpm.nodesource.com/setup_6.x | bash - 
RUN yum install -y nodejs \
	&& yum install -y git \
        && npm install --save guacamole-lite 
RUN git clone https://github.com/bpeters-cmu/node_guac.git

WORKDIR /node_guac/
EXPOSE 8291

CMD guacd start && node NodeServer/node_server.js

