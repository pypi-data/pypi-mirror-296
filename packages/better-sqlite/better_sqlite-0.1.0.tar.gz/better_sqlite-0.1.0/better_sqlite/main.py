from __future__ import annotations

import sqlite3
from typing import Any, Dict, Optional


class Database:
    """
    A simple SQLite wrapper that provides an easier interface for interacting with
    SQLite databases.

    This class supports basic CRUD operations such as creating tables, inserting data,
    retrieving data, updating records, and deleting rows without the need to write raw SQL.

    It also supports being used as a context manager to ensure the database connection
    is properly managed.
    """

    def __init__(self, db_path: str) -> None:
        """
        Initializes the Database class with a given database path.

        Args:
            db_path (str): The path to the SQLite database file.
        """

        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def __enter__(self) -> Database:
        """
        Opens the database connection and returns the Database instance for use
        in a context manager.

        Returns:
            Database: The instance of the Database class with an open connection.
        """

        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Closes the database connection when exiting the context manager.
        If no exception occurred, it commits the changes.

        Args:
            exc_type: The type of exception raised (if any).
            exc_value: The value of the exception raised (if any).
            traceback: The traceback object of the exception (if any).
        """

        if self.conn:
            if exc_type is None:
                self.conn.commit()  # Commit the changes only if no exception

            self.conn.close()

    def create_table(self, table_name, schema: Dict[str, str]) -> None:
        """
        Creates a table with the specified schema.

        Args:
            table_name (str): The name of the table to be created.
            schema (Dict[str, str]): A dictionary representing the table schema,
            where keys are column names and values are
            SQLite data types (e.g., "TEXT", "INTEGER").

        Example:
            >>> schema = {"name": "TEXT", "age": "INTEGER"}
            >>> db.create_table("users", schema)
        """

        columns = ", ".join(
            [f"{name} {data_type}" for name, data_type in schema.items()]
        )
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})")

    def insert(self, table_name: str, data: Dict[str, Any]):
        """
        Inserts a row of data into the specified table.

        Args:
            table_name (str): The name of the table to insert data into.
            data (Dict[str, Any]): A dictionary representing the data to be inserted,
            where keys are column names and values are the values to be inserted.

        Example:
            >>> db.insert("users", {"name": "Alice", "age": 30})
        """

        columns = ", ".join(data.keys())
        placeholders = ", ".join("?" for _ in data)
        self.cursor.execute(
            f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})",
            tuple(data.values()),
        )

    def get(
        self, table_name: str, conditions: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves a single row from the specified table that matches the given conditions.

        Args:
            table_name (str): The name of the table to query.
            conditions (Dict[str, Any]): A dictionary of conditions to filter the query,
            where keys are column names and values are the values to match.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the row if found,
            where keys are column names and values are the corresponding values from the
            database, or None if no row is found.

        Example:
            >>> user = db.get("users", {"name": "Alice"})
        """

        condition_string = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        self.cursor.execute(
            f"SELECT * FROM {table_name} WHERE {condition_string}",
            tuple(conditions.values()),
        )
        row = self.cursor.fetchone()

        if row:
            column_names = [description[0] for description in self.cursor.description]
            return {column: value for column, value in zip(column_names, row)}

        return None

    def update(
        self, table_name: str, values: Dict[str, Any], conditions: Dict[str, Any]
    ) -> None:
        """
        Updates rows in the specified table that match the given conditions
        with new values.

        Args:
            table_name (str): The name of the table to update.
            values (Dict[str, Any]): A dictionary representing the columns and values
            to update.
            conditions (Dict[str, Any]): A dictionary of conditions to filter the update,
            where keys are column names and values are the values to match.

        Example:
            >>> db.update("users", {"age": 31}, {"name": "Alice"})
        """

        set_string = ", ".join([f"{key} = ?" for key in values.keys()])
        condition_string = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        self.cursor.execute(
            f"UPDATE {table_name} SET {set_string} WHERE {condition_string}",
            tuple(values.values()) + tuple(conditions.values()),
        )

    def delete(self, table_name: str, conditions: Dict[str, Any]) -> None:
        """
        Deletes rows from the specified table that match the given conditions.

        Args:
            table_name (str): The name of the table to delete from.
            conditions (Dict[str, Any]): A dictionary of conditions to filter the delete,
            where keys are column names and values are the values to match.

        Example:
            >>> db.delete("users", {"name": "Alice"})
        """

        condition_string = " AND ".join([f"{key} = ?" for key in conditions.keys()])
        self.cursor.execute(
            f"DELETE FROM {table_name} WHERE {condition_string}",
            tuple(conditions.values()),
        )
