FROM python:3.9

RUN \
     apt-get update && apt-get -y install \
         ffmpeg libpq-dev && \
     apt-get clean && \
     rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install --upgrade pip -r requirements.txt

COPY . /app

EXPOSE 5000