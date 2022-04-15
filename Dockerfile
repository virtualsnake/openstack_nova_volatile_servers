FROM python:3.10

COPY requirements.txt ./requirements.txt
COPY app/ ./

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]