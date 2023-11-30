#Using slim for small size container
FROM python:3.9.15-slim-buster
#META
LABEL NAME="angyay0/stock-take-home"
LABEL MAINTAINER="Angel Perez"
#Disable Byte code
ENV PYTHONDONTWRITEBYTECODE 1
#Disable Buffer
ENV PYTHONUNBUFFERED 1
#Configure Production Mode
ENV ENV "prod"
#Confiure api Port number
ENV PORT 5001
#Disable Debug Flask 
ENV FLASK_DEBUG 0
#Adding Files and setting up wdir
COPY . /api
WORKDIR /api
#Installing Requirements
RUN apt-get update && apt-get -y install libpq-dev gcc && pip install psycopg2
RUN pip3 install -r requirements.txt
#Export Port
EXPOSE ${PORT}
#Configuring Entry Point
ENTRYPOINT ["python3"]
#Run
CMD ["main.py","docker_run"]