from abc import ABC
import re
import sqlite3


class SqliteRepository(ABC):
    """Base class for all sqlite repositories"""

    def __init__(self, base_path: str):
        self.base_path = base_path

    def _query_cleaner(self, query: str) -> str:
        """Clean query"""
        query = query.strip()
        query = query.replace("\n", " ")
        query = query.replace("\t", " ")
        query = re.sub(" +", " ", query)
        return query

    def _execute_statement(
        self, target_database: str, statement: str, parameters: tuple = ()
    ) -> None:
        """Execute a statement on the target database"""
        statement = self._query_cleaner(statement)

        with sqlite3.connect(
            f"{self.base_path}/{target_database}.sqlite"
        ) as index_connection:
            index_cursor = index_connection.cursor()
            index_cursor.execute(statement, parameters)
            index_connection.commit()

    def _execute_query(
        self, target_database: str, statement: str, parameters: tuple = ()
    ) -> list:
        """Execute a query on the target database"""
        statement = self._query_cleaner(statement)

        with sqlite3.connect(
            f"{self.base_path}/{target_database}.sqlite"
        ) as index_connection:
            index_cursor = index_connection.cursor()
            result = index_cursor.execute(statement, parameters)
            return result.fetchall()
