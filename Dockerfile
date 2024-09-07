FROM python:3.7
RUN apt-get update && \
    apt-get install -y \
    build-essential \
    cmake \
    git \
    sudo \
    wget \
    vim

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /

COPY ./ .

ENV FLASK_APP=app.py

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000",  "app:app"]