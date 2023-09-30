FROM i386/python:3.10.6-alpine

ENV APP_HOME="/root/src"

RUN mkdir $APP_HOME
COPY . $APP_HOME/
RUN ls $APP_HOME

RUN pip install -r $APP_HOME/requirements.txt

RUN apk add curl

EXPOSE 5000

ENTRYPOINT ["python3", "/root/src/main.py"]
