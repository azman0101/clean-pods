FROM python:3.13.0a3-slim@sha256:c4d327c9040a33bbd59b90d17daed18e6e837ef9c4ac66a2af3b75cc5e1ee650

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
