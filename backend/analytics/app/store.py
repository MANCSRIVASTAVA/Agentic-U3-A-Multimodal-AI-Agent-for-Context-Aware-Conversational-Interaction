import os, hashlib
from datetime import datetime
from typing import Dict, List
from clickhouse_driver import Client


def get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


class ClickHouseStore:
    def __init__(self, host: str, port: int, database: str, user: str, password: str):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

        # Client with DB (usable after ensure_schema runs)
        self.client = Client(
            host=self.host,
            port=self.port,
            database=self.database,
            user=self.user,
            password=self.password,
            settings={"use_numpy": False},
        )

    @classmethod
    def from_env(cls) -> "ClickHouseStore":
        host = get_env("CLICKHOUSE_HOST", "clickhouse")
        port = int(get_env("CLICKHOUSE_PORT", "9000"))
        db = get_env("CLICKHOUSE_DB", "analytics")
        user = get_env("CLICKHOUSE_USER", "default")
        pwd = get_env("CLICKHOUSE_PASSWORD", "")
        return cls(host, port, db, user, pwd)

    def ensure_schema(self):
        """
        Idempotent bootstrap:
          1. Connect without selecting a DB -> CREATE DATABASE IF NOT EXISTS
          2. Reconnect with DB -> CREATE TABLE IF NOT EXISTS
        """
        # Step 1: client without database
        c0 = Client(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            settings={"use_numpy": False},
        )
        c0.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")

        # Step 2: create events table in the target DB
        self.client.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {self.database}.events (
                event_id       String,
                session_id     String,
                correlation_id String,
                type           String,
                ts             DateTime64(3, 'UTC'),
                latencies      Map(String, Float64),
                usage          Map(String, Float64),
                flags          Map(String, UInt8),
                labels         Map(String, String)
            )
            ENGINE = ReplacingMergeTree()
            ORDER BY (event_id, session_id, ts)
            """
        )

    # ----------------- Helpers -----------------

    def compute_event_id(self, session_id: str, correlation_id: str, etype: str) -> str:
        return hashlib.md5(f"{session_id}|{correlation_id}|{etype}".encode("utf-8")).hexdigest()

    def event_exists(self, event_id: str) -> bool:
        q = f"SELECT count() FROM {self.database}.events WHERE event_id = %(event_id)s"
        cnt = self.client.execute(q, {"event_id": event_id})[0][0]
        return cnt > 0

    def insert_event(
        self,
        event_id: str,
        session_id: str,
        correlation_id: str,
        type: str,
        ts: datetime,
        latencies: Dict[str, float],
        usage: Dict[str, float],
        flags: Dict[str, int],
        labels: Dict[str, str],
    ):
        q = f"""
        INSERT INTO {self.database}.events
            (event_id, session_id, correlation_id, type, ts, latencies, usage, flags, labels)
        VALUES
        """
        self.client.execute(
            q, [(event_id, session_id, correlation_id, type, ts, latencies, usage, flags, labels)]
        )

    def fetch_session_events(self, session_id: str) -> List[dict]:
        q = f"""
        SELECT event_id, session_id, correlation_id, type, ts, latencies, usage, flags, labels
        FROM {self.database}.events
        WHERE session_id = %(sid)s
        ORDER BY ts ASC
        """
        rows = self.client.execute(q, {"sid": session_id}, with_column_types=True)
        cols = [c[0] for c in rows[1]]
        return [{cols[i]: r[i] for i in range(len(cols))} for r in rows[0]]


def get_store() -> ClickHouseStore:
    return ClickHouseStore.from_env()
