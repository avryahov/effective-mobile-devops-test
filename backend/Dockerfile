FROM python:3.12-alpine AS builder

WORKDIR /app

COPY app.py start.sh /app/

FROM python:3.12-alpine

WORKDIR /app

RUN addgroup -S app && adduser -S app -G app

COPY --from=builder /app/app.py /app/app.py
COPY --from=builder /app/start.sh /app/start.sh

RUN chmod 0555 /app/start.sh /app/app.py

USER app

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/healthz', timeout=2)"

ENTRYPOINT ["/app/start.sh"]
