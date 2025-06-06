import os
import json

from pathlib import Path

from dotenv import load_dotenv


def main():
    load_dotenv()

    config = {
        "name": "postgres-connector",
        "config": {
            "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
            "database.hostname": os.getenv("DB_HOST"),
            "database.port": os.getenv("DB_PORT"),
            "database.user": os.getenv("DB_USER"),
            "database.password": os.getenv("DB_PASSWORD"),
            "database.dbname": os.getenv("DB_NAME"),
            "database.server.name": os.getenv("DB_SERVER_NAME"),
            "table.include.list": os.getenv("DB_TABLE"),
            "plugin.name": "pgoutput",
            "slot.name": os.getenv("DB_SLOT_NAME"),
            "key.converter": "io.confluent.connect.avro.AvroConverter",
            "key.converter.schema.registry.url": os.getenv("SCHEMA_REGISTRY_URL"),
            "value.converter": "io.confluent.connect.avro.AvroConverter",
            "value.converter.schema.registry.url": os.getenv("SCHEMA_REGISTRY_URL")
        }
    }
    try:
        root_path = Path(os.getenv("ROOT_PATH"))
    except TypeError:
        root_path = Path(__file__).parent.parent.parent
    except KeyError:
        root_path = Path(__file__).parent.parent
    config_path = root_path / 'register-postgres.json'
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


if __name__ == "__main__":
    main()
