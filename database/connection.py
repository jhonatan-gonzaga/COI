"""Conexao com PostgreSQL usando psycopg2."""

import os

import psycopg2
from dotenv import load_dotenv


load_dotenv()


def get_database_config(database=None):
    return {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": os.getenv("DB_PORT", "5432"),
        "dbname": database or os.getenv("DB_NAME", "conecta_obras"),
        "user": os.getenv("DB_USER", "postgres"),
        "password": os.getenv("DB_PASSWORD", "postgres"),
    }


def get_connection(database=None):
    return psycopg2.connect(**get_database_config(database))


def test_connection():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT 1")
            return cur.fetchone()[0] == 1
    finally:
        conn.close()
