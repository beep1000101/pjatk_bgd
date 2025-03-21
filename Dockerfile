FROM python:3.12

WORKDIR /app

COPY . /app

RUN --mount=type=cache,target=/root/.cache/pip pip install --no-cache-dir -r requirements.txt

ENV DB_USERNAME=postgres \
    DB_PASSWORD=postgrespassword \
    DB_HOST=localhost \
    DB_NAME=bgddatabase

# Komenda uruchamiająca skrypt
CMD ["python", "__main__.py"]