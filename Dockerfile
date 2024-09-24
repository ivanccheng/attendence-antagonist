
FROM python:3.8-slim-buster
ENV WORKDIR=/user/src/app
RUN mkdir -p $WORKDIR
WORKDIR $WORKDIR
COPY "./*" $WORKDIR/
RUN pip3 install -r requirements.txt
ENTRYPOINT ["./gunicorn.sh"]

# Port is supplied by heroku 
EXPOSE $PORT