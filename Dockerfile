FROM python:3.10

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY volatile_api/ ./volatile_api

CMD ["python", "volatile_api/app.py"]