FROM python:3.10.6-slim-buster

LABEL maintainer="Asante, Yeboah Gideon <asanteg36@gmail.com>"

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "gunicorn", "-b 0.0.0.0:8000" ,"run:app" ]