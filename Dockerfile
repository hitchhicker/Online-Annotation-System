FROM python:3.5-jessie
MAINTAINER YU Bokai <yubokai8@gmail.com>

ADD requirements.txt .
RUN pip install -r requirements.txt

RUN mkdir -p /var/www/app
COPY online_annotation_system /var/www/app/online_annotation_system

WORKDIR /var/www/app/online_annotation_system
RUN mkdir -p data/xmls
RUN mkdir -p data/images

EXPOSE 8000

CMD ["python", "server.py"]