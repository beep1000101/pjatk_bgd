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
            "database.hostname": os.getenv("DB_HOST", "postgres"),
            "database.port": os.getenv("DB_PORT", "5432"),
            "database.user": os.getenv("DB_USER", "postgres"),
            "database.password": os.getenv("DB_PASSWORD", "postgres"),
            "database.dbname": os.getenv("DB_NAME", "mydb"),
            "database.server.name": os.getenv("DB_SERVER_NAME", "mydb_server"),
            "table.include.list": os.getenv("DB_TABLE", "public.orders,public.users"),
            "plugin.name": "pgoutput",
            "slot.name": os.getenv("DB_SLOT_NAME", "debezium_slot"),
            "topic.prefix": os.getenv("DB_TOPIC_PREFIX", "dbserver1"),
            "key.converter": "org.apache.kafka.connect.json.JsonConverter",
            "value.converter": "org.apache.kafka.connect.json.JsonConverter",
            "key.converter.schemas.enable": "false",
            "value.converter.schemas.enable": "false"
        }
    }
    try:
        root_path = Path(os.getenv("ROOT_PATH", str(
            Path(__file__).parent.parent.parent)))
    except TypeError:
        root_path = Path(__file__).parent.parent.parent
    except KeyError:
        root_path = Path(__file__).parent.parent
    config_path = root_path / 'register-postgres.json'
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


if __name__ == "__main__":
    main()
