FROM python:3.11

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY . /app/
WORKDIR /app/

ENV PYTHONPATH=/app

CMD ["python", "/app/main.py"]