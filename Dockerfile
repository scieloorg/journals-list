FROM python:3.5.3-slim
LABEL manintainer "ednilson.gesseff@scielo.org"

COPY . /app 

WORKDIR /app

RUN cp /usr/share/zoneinfo/America/Sao_Paulo /etc/localtime
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD python journals-list.py
