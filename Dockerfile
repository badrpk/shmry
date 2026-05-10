FROM python:3.12-slim
WORKDIR /app
RUN apt-get update && apt-get install -y sqlite3 curl jq git && rm -rf /var/lib/apt/lists/*
COPY . /app
EXPOSE 8088
CMD ["python3", "observability/dashboard.py"]
