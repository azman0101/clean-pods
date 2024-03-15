FROM python:3.13.0a5-slim@sha256:4024be4854155da68418c0e6fd62f3b58637aef6946c5e9be101edb919f2ec8a

ENV API_URL="https://kubernetes.default.svc/"
ENV NAMESPACE="gitlab"
ENV MAX_HOURS="1"
ENV POD_STATUS="Succeeded, Failed"
ENV TOKEN=""
ENV STARTS_WITH="runner-"

ENV PYTHONUNBUFFERED=0

WORKDIR /app
COPY ./app/ ./
COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt
USER 1
CMD ["/usr/local/bin/python", "/app/clean.py"]
