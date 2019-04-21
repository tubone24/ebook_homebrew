FROM centos
MAINTAINER tubone24 <tubo.yyyuuu@gmail.com>

RUN yum update
RUN yum install -y git python
RUN mkdir /app
COPY ebook_homebrew/. /app
RUN python setup.py install
