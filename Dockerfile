FROM apache/airflow:3.0.6
COPY requirements.txt .
RUN pip install -r requirements.txt