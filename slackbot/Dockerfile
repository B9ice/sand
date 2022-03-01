# syntax=docker/dockerfile:1
FROM python:3-slim

RUN apt-get update && apt-get install gcc -y && apt-get clean

RUN apt-get update && apt-get install -y python
RUN python -m pip install --upgrade pip

ADD . /slack-test/

WORKDIR /slack-test

RUN pip install -r requirements.txt

ENV TZ="America/New_York"

# CMD [ "python3", "-m", "pytest", "--no-header", "-vv", "--no-summary", "-q", "tests",  "--html=report.html"]