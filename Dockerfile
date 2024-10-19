FROM python:3.13.0-slim@sha256:751d8bece269ba9e672b3f2226050e7e6fb3f3da3408b5dcb5d415a054fcb061

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
