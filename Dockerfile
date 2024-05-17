FROM python:3.11.4-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# set working dir
WORKDIR /code

# copy requirement.txt first to hit the cache
ADD requirements.txt /code/

# upgrade pip wheel and setuptools then install requirements
RUN pip install --no-cache-dir --upgrade pip wheel setuptools &&  \
    pip install --no-cache-dir -r requirements.txt

COPY . .
