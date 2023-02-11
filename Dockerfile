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

EXPOSE 8000

# CMD ["bash", "run.sh"]

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]