FROM tuki0918/dev-python:latest

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt
