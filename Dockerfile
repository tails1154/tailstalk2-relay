# TailsTalk 2 PS4 relay: plain TCP in, TLS out to the events service
FROM docker.io/library/python:3.12-slim
WORKDIR /app
COPY ws_relay.py /app/ws_relay.py
EXPOSE 9963
CMD ["python3", "/app/ws_relay.py", "--listen", "0.0.0.0:9963"]
