import os

serial_port="/dev/ttyUSB0"

#influx db
host=os.environ['DB_HOST']
port=os.environ['DB_PORT']
username=os.environ['DB_USER']
password=os.environ['DB_PASSWORD']
database=os.environ['DB_NAME']

DDS353H_ids=os.environ['DDS353H_IDS'].split(",")
YTL5300_ids=os.environ['YTL5300_IDS'].split(",")
