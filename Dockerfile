
FROM python:3.8-slim-buster
ENV WORKDIR=/user/src/app
RUN mkdir -p $WORKDIR
COPY "." $WORKDIR
RUN apt-get update 
RUN apt-get -y install libpq-dev gcc 
RUN pip3 install -r requirements.txt
ENTRYPOINT ["./gunicorn.sh"]

# Port is supplied by heroku 
EXPOSE $PORT