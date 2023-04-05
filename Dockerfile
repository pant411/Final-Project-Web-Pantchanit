FROM python:3.8-slim-buster

RUN mkdir /myapp

COPY . /myapp

WORKDIR /myapp

ENV TZ="Asia/Bangkok"
# ENV PYTHONUNBUFFERED True

RUN apt-get update && \
    apt-get install -y \
        build-essential \
        python3-dev \
        python3-setuptools \
        make \
        ffmpeg \
        libsm6 \
        libxext6 \
        gcc && \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r /myapp/requirements.txt     

# RUN chmod 744 /myapp/static/css
# RUN chmod 744 /myapp/static/js

# EXPOSE 8080

# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
CMD gunicorn -b :$PORT main:app -k uvicorn.workers.UvicornWorker --workers 4 --timeout 0
