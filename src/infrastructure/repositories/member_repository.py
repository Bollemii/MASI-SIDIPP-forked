from datetime import datetime
import sqlite3
from typing import Literal

from src.infrastructure.repositories.common.sqlite_repository import SqliteRepository
from src.application.exceptions.member_already_exists_error import (
    MemberAlreadyExistsError,
)
from src.application.interfaces.imember_repository import IMemberRepository
from src.domain.entities.member import Member


class MemberRepository(IMemberRepository, SqliteRepository):
    """Sqlite implementation of the member repository class"""

    def initialize_if_not_exists(self, target_database: str):
        self._execute_statement(
            target_database,
            """CREATE TABLE IF NOT EXISTS nodes_relationships (
                relationship_id TEXT CONSTRAINT nodes_relationships_pk PRIMARY KEY
            );""",
        )
        self._execute_statement(
            target_database,
            """CREATE TABLE IF NOT EXISTS nodes (
                authentication_key TEXT CONSTRAINT nodes_pk PRIMARY KEY,
                ip_address TEXT NOT NULL,
                port INTEGER NOT NULL,
                creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                last_connection_date DATE,
                relationship_id TEXT CONSTRAINT nodes_fk REFERENCES nodes_relationships
            );""",
        )
        self._execute_statement(
            target_database,
            """INSERT OR IGNORE INTO nodes_relationships (relationship_id)
                VALUES ('parent'), ('child');
            """,
        )

    def add_member_to_community(
        self,
        community_id: str,
        member: Member,
        relationship: Literal["parent", "child"] | None = None,
    ) -> None:
        self.initialize_if_not_exists(community_id)

        try:
            self._execute_statement(
                community_id,
                """INSERT INTO nodes (
                    authentication_key,
                    ip_address,
                    port,
                    creation_date,
                    last_connection_date,
                    relationship_id
                ) VALUES (?, ?, ?, ?, ?, ?);""",
                (
                    member.authentication_key,
                    member.ip_address,
                    member.port,
                    member.creation_date.isoformat(),
                    (
                        member.last_connection_date.isoformat()
                        if member.last_connection_date is not None
                        else None
                    ),
                    relationship,
                ),
            )
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: nodes.authentication_key" in str(error):
                raise MemberAlreadyExistsError(error) from error

    def clear_members_relationship(
        self,
        community_id: str,
    ) -> None:
        self.initialize_if_not_exists(community_id)

        self._execute_statement(
            community_id,
            """UPDATE nodes SET relationship_id = NULL;""",
        )

    def update_member_relationship(
        self,
        community_id: str,
        auth_key: str,
        relationship: Literal["parent", "child"] | None,
    ) -> None:
        self.initialize_if_not_exists(community_id)

        self._execute_statement(
            community_id,
            """UPDATE nodes
            SET relationship_id = ?
            WHERE authentication_key = ?;""",
            (relationship, auth_key),
        )

    def get_member_for_community(
        self,
        community_id: str,
        member_auth_key: str | None = None,
        ip_address: str | None = None,
    ) -> Member | None:
        self.initialize_if_not_exists(community_id)

        if member_auth_key is None and ip_address is None:
            raise ValueError("Either member_auth_key or ip_address must be specified")

        if member_auth_key is not None and ip_address is not None:
            condition = "WHERE authentication_key = ? AND ip_address = ?"
            parameters = (member_auth_key, ip_address)
        elif member_auth_key is not None:
            condition = "WHERE authentication_key = ?"
            parameters = (member_auth_key,)
        else:
            condition = "WHERE ip_address = ?"
            parameters = (ip_address,)

        result = self._execute_query(
            community_id,
            """SELECT
            authentication_key,
            ip_address,
            port,
            creation_date,
            last_connection_date
            FROM nodes """
            + condition
            + ";",
            parameters,
        )

        if len(result) == 0:
            return None

        (
            authentication_key,
            ip_address,
            port,
            creation_date,
            last_connection_date,
        ) = result[0]
        return Member(
            authentication_key,
            ip_address,
            port,
            datetime.fromisoformat(creation_date),
            (
                None
                if last_connection_date is None
                else datetime.fromisoformat(last_connection_date)
            ),
        )

    def get_members_from_community(
        self, community_id: str, is_related: bool = False
    ) -> list[Member]:
        """Get all members from a community."""
        self.initialize_if_not_exists(community_id)

        statement = """SELECT
            authentication_key,
            ip_address,
            port,
            creation_date,
            last_connection_date
            FROM nodes""" + (
            " WHERE relationship_id IS NOT NULL;" if is_related else ";"
        )

        result = self._execute_query(
            community_id,
            statement,
        )

        members = []
        for (
            authentication_key,
            ip_address,
            port,
            creation_date,
            last_connection_date,
        ) in result:
            members.append(
                Member(
                    authentication_key,
                    ip_address,
                    port,
                    datetime.fromisoformat(creation_date),
                    (
                        None
                        if last_connection_date is None
                        else datetime.fromisoformat(last_connection_date)
                    ),
                )
            )

        return members
