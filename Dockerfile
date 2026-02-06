FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt pyproject.toml README.md /app/
COPY src /app/src
COPY rules /app/rules

RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir -e .

ENTRYPOINT ["sis"]
CMD ["--help"]
