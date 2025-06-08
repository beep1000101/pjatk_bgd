# Mini Data Platform – README

## Autor: Mateusz Poniatowski

### Poziom zabawy: Wysoki

### Poziom złożoności poznawczej narzędzi użytych w projekcie: Wysoki

## TL;DR

1. **Klonowanie repozytorium**:

   ```bash
   git clone https://github.com/beep1000101/pjatk_bgd.git && cd pjatk_bgd
   ```
2. **Instalacja zależności Python**:

   ```bash
   pip install -r requirements.txt
   ```
3. **Uruchomienie testów jednostkowych (pytest)**:

   ```bash
   pytest
   ```
4. **Zbudowanie i uruchomienie kontenerów Docker**:

   ```bash
   docker-compose up --build
   ```
5. **Sprawdzenie stanu usług (health checks)**:

   ```bash
   python3 scripts/health_checks/docker/check_all.py
   ```


# Mini Data Platform – README

## 1. Opis projektu

Projekt dostarcza kontenerową mini platformę danych, uruchamianą w Dockerze, ukazując kompletny pipeline od generacji i symulacji danych aż po ich ekspozycję i przetwarzanie:

1. **Symulacja procesów biznesowych** – skrypty Python 3.13 czytające pliki CSV z katalogu `data/`.
2. **Flask API** – aplikacja we Flask (`flask_app/`) udostępniająca REST-owe endpointy do odczytu danych.
3. **PostgreSQL** – baza danych z włączoną replikacją logiczną (skrypty w `database/`).
4. **Debezium Connector** – kontener Kafka Connect nasłuchujący zmian w PostgreSQL i wysyłający je do Kafki.
5. **Kafka Broker** – system kolejkowania wiadomości w formacie **JSON** (AVRO nie został wdrożony, JSON działa stabilnie i upraszcza konfigurację).
6. **Spark Streaming** – aplikacja Spark (`spark_app/`) przetwarzająca strumień z Kafki i wykonująca transformacje.
7. **Narzędzia pomocnicze** – skrypty health checks (`scripts/health_checks/`), narzędzia Kafka (`Dockerfile.kafka-tools`) itp.

## 2. Wymagania

* **Docker** ≥ 20.10
* **Docker Compose** ≥ 1.29
* **Python** **3.13**
* **Pip dependencies** (uruchomienie `pip install -r requirements.txt`)

## 3. Architektura

```
[ Symulacja danych ] -> [ Flask API ] -> [ PostgreSQL ] -> [ Debezium ] -> [ Kafka (JSON) ] -> [ Spark Streaming ]
```

* **Symulacja danych**: skrypty w `scripts/` pobierają pliki CSV z `data/orders/` i `data/users/`, inicjalizują i seedują bazę.
* **Flask API**: `flask_app/app.py` udostępnia endpointy `/users` i `/orders`, wykorzystując SQLAlchemy (`flask_app/schemas/`).
* **PostgreSQL**: konfiguracja w `database/config.py`, skrypty inicjalizacyjne w `database/initdb` oraz `init_replication.sql`.
* **Debezium Connector**: definiowany w kontenerze `docker-compose.yml` z użyciem `Dockerfile.connect` i `Dockerfile.connector-registrator`.
* **Kafka**: broker oraz narzędzia (`kafka-tools`) w osobnych kontenerach, topiki tworzone automatycznie przez Debezium.
* **Format wiadomości**: wszystkie komunikaty w JSON (AVRO zostało przetestowane — plik JAR w `etc/kafka/connect/jars/`, ale ostatecznie nie wdrożone).
* **Spark Streaming**: aplikacja w `spark_app/app.py` subskrybuje temat Kafki, przetwarza dane i może zapisywać rezultaty do zewnętrznych systemów (np. MinIO, jeśli dodany).
* **Monitoring**: skrypty w `scripts/health_checks/` (m.in. `check_postgres.py`, `check_connect.py`, `check_zookeeper.py`) pomagają w bieżącej diagnostyce.

## 4. Uruchomienie

1. Sklonuj repozytorium i przejdź do katalogu:

   ```bash
   git clone https://github.com/beep1000101/pjatk_bgd.git && cd pjatk_bgd
   ```
2. Zbuduj i uruchom usługi:

   ```bash
   docker-compose up --build
   ```
3. Zweryfikuj działające kontenery:

   ```bash
   docker-compose ps
   ```

## 5. Dostęp do usług

* **PostgreSQL**: `localhost:5432`, DB=`business`, user=`postgres`, pass=`postgres`
* **Kafka Broker**: `localhost:9092`
* **Spark UI**: `http://localhost:4040`
* **Flask API**: `http://localhost:5000`

## 6. Skrypty i przykłady

| Skrypt                                      | Opis                                            | Uruchomienie                                                                                                               |
| ------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------- |
| `scripts/simulate_business.py`              | Generuje i wstawia dane do PostgreSQL           | `python3 scripts/simulate_business.py`                                                                                     |
| `scripts/health_checks/docker/check_all.py` | Sprawdza stan wszystkich usług Docker           | `python3 scripts/health_checks/docker/check_all.py`                                                                        |
| `scripts/kafka_check.sh`                    | Prosty skrypt bash do weryfikacji brokera Kafka | `bash scripts/kafka_check.sh`                                                                                              |
| `spark_app/app.py`                          | Aplikacja Spark Streaming                       | `spark-submit --packages io.delta:delta-core_2.12:1.2.1,org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1 spark_app/app.py` |

---

*Projekt przygotowany na Pythonie 3.13.* Próba integracji z AVRO niestety się nie powiodła, dlatego pozostała komunikacja odbywa się w JSON – stabilna i wystarczająca alternatywa dla AVRO. komunikacja Debezium→Kafka odbywa się w JSON – stabilna i wystarczająca alternatywa dla AVRO.\*
