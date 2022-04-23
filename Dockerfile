FROM python:3.10

COPY requirements.txt ./
COPY volatile_api/ ./

RUN pip install -r requirements.txt

RUN chmod +x ./start.sh
CMD ["./start.sh"]