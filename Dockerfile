FROM python:3.10

WORKDIR /project

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY volatile_api/ ./volatile_api

ENV PYTHONPATH=/project
CMD ["python", "volatile_api/app.py"]