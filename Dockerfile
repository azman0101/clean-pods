FROM python:3.13.0a5-slim@sha256:fe45ff0c45c5063b3e5d0f2bdac6564016a7d5faeda5ff9660c74c4b987500c6

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
