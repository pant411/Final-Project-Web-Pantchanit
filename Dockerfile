FROM python:3.8-slim-buster

RUN mkdir /myapp

COPY . /myapp

WORKDIR /myapp

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        tesseract-ocr \
        tesseract-ocr-tha \
        make \
        ffmpeg \
        libsm6 \
        libxext6 \
        gcc && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /myapp/library_list.txt         

CMD ["bash", "run.sh"]