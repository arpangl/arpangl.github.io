FROM python:3.9-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends g++ && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY judge.py server.py problems_list.json ./
COPY web/ ./web/
COPY problems/ ./problems/

EXPOSE 5269

CMD ["python3", "server.py", "--host", "0.0.0.0", "--port", "5269"]
