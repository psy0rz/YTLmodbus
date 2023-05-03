FROM python:3.11-alpine

WORKDIR /app
COPY  requirements.txt /app/
RUN pip install -r /app/requirements.txt

COPY config.py ytl.py /app/
CMD python -u ytl.py




