# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m venv /opt/venv && \
    /bin/bash -c "source /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt"

COPY . .

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["pytest"]
