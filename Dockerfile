FROM python:3.13.0a4-slim@sha256:664a24153d53a7a94fac6c52b1f2bb2283385df23135edf802fbf97a2cc64b36

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
