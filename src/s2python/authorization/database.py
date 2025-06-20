"""
Database handler for storing and verifying S2 challenges.
"""

import sqlite3
import logging
from contextlib import contextmanager
from typing import Generator

logger = logging.getLogger(__name__)


class S2Database:
    """Handles the SQLite database for challenges."""

    def __init__(self, db_path: str):
        """
        Initialize the ChallengeDatabase.

        :param db_path: The path to the SQLite database file.
        """
        self.db_path = db_path
        self.init_db()

    @contextmanager
    def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Provides a database connection."""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def init_db(self) -> None:
        """Initializes the database and creates the 'challenges' table if it doesn't exist."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS challenges (
                    challenge TEXT PRIMARY KEY,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS key_pairs (
                    id INTEGER PRIMARY KEY,
                    public_key TEXT NOT NULL,
                    private_key TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """
            )

            conn.commit()
        logger.info("Database initialized at %s", self.db_path)

    def store_challenge(self, challenge: str) -> None:
        """
        Stores a challenge in the database.

        :param challenge: The challenge string to store.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO challenges (challenge) VALUES (?)", (challenge,))
            conn.commit()
        logger.info("Stored challenge in the database.")

    def store_key_pair(self, public_key: str, private_key: str) -> None:
        """
        Stores a key pair in the database.

        :param public_key: The public key string to store.
        :param private_key: The private key string to store.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO key_pairs (public_key, private_key) VALUES (?, ?)", (public_key, private_key))
            conn.commit()
        logger.info("Stored key pair in the database.")

    def verify_and_remove_challenge(self, challenge: str) -> bool:
        """
        Verifies a challenge exists and removes it to prevent reuse.

        :param challenge: The challenge string to verify.
        :return: True if the challenge was valid, False otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT challenge FROM challenges WHERE challenge=?", (challenge,))
            result = cursor.fetchone()
            if result:
                logger.info("Challenge found. Removing it from database.")
                cursor.execute("DELETE FROM challenges WHERE challenge=?", (challenge,))
                conn.commit()
                return True
            logger.warning("Challenge not found in database.")
            return False
