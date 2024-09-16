from contextlib import contextmanager
from threading import Lock
from typing import Generator, Optional

from neo4j import Driver, GraphDatabase, Session

from neurapolis_common.config import config


class DbSessionBuilder:
    def __init__(self):
        self._driver: Optional[Driver] = None
        self._lock = Lock()

    @contextmanager
    def build(self) -> Generator[Session, None, None]:
        with self._lock:
            if self._driver == None:
                self._driver = GraphDatabase.driver(
                    config.db_uri, auth=(config.db_username, config.db_password)
                )
        try:
            with self._driver.session(database=config.db_name) as session:
                yield session
        finally:
            pass

    def close(self):
        with self._lock:
            if self._driver != None:
                self._driver.close()
                self._driver = None


db_session_builder = DbSessionBuilder()
