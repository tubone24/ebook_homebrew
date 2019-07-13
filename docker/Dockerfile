FROM centos:centos7
MAINTAINER tubone24 <tubo.yyyuuu@gmail.com>

## install util
RUN yum -y update \
 && yum -y install \
     epel-release \
     gcc \
     git \
     vim \
     which \
     && yum clean all

# https://www.python.jp/install/centos/index.html
RUN yum install -y https://centos7.iuscommunity.org/ius-release.rpm
RUN yum install -y \
     python36u \
     python36u-devel \
     python36u-pip \
 && yum clean all \
 && ln -sf /usr/bin/python3.6 /usr/bin/python3 \
 && ln -sf /usr/bin/pip3.6 /usr/bin/pip3 \
 && pip3 install --upgrade pip

# setup node.js

RUN yum -y install nodejs npm
RUN npm install -g n
RUN n stable && node -v


# setup ebook-homebrew
RUN mkdir /app
RUN cd /app && git clone https://github.com/tubone24/ebook_homebrew.git && cd ebook_homebrew \
  && git submodule update --init --recursive
WORKDIR /app/ebook_homebrew
RUN pip3 install -r requirements.txt

# setup vue client
RUN rm ebook_homebrew/static/index.html
RUN cd examples/ebook-homebrew-vue-client && npm install && npm run build
RUN cp examples/ebook-homebrew-vue-client/dist/index.html ebook_homebrew/static/
RUN mkdir -p ebook_homebrew/static/static/static
RUN cp -r examples/ebook-homebrew-vue-client/dist/static ebook_homebrew/static/static/

# install ebook-homebrew
RUN python3 setup.py install

CMD ebookhomebrew api -p ${PORT}
