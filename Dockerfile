FROM ubuntu:14.04
MAINTAINER YU Bokai <yubokai8@gmail.com>
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y \
    build-essential python \
    libevent-dev \
    python3-dev \
    python-dev \
    python3.4 \
    libtiff5-dev \
    libjpeg8-dev \
    zlib1g-dev \
    libfreetype6-dev \
    liblcms2-dev \
    libwebp-dev \
    tcl8.6-dev \
    tk8.6-dev \
    python-tk \
    && rm -rf /var/lib/apt/lists/*

RUN sudo apt-get update
RUN sudo apt-get install -y python3-pip
RUN sudo apt-get install -y python-pip

ADD requirements.txt .
RUN pip3 install -r requirements.txt

RUN mkdir -p /var/www/app
COPY . /var/www/app
WORKDIR /var/www/app
ENV PYTHONPATH /var/www/app/

ENV PATH /usr/bin/python3.4:$PATH:
ENTRYPOINT ["python3"]
CMD ["server.py"]