FROM python:3.8-slim-buster

RUN mkdir /myapp

COPY . /myapp

WORKDIR /myapp

ENV PYTHONUNBUFFERED True

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

EXPOSE 8080

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

# CMD exec gunicorn --bind :8080 --workers 1 --threads 8 --timeout 0 app:app

# CMD gunicorn --bind :$PORT app:app