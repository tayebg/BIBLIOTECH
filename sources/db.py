# -*- coding: utf-8 -*-
"""
Database Abstraction Layer for BIBLIOTECH
Supports PostgreSQL (default) and SQLite3 with seamless fallback.
"""

import os
import sys
from typing import Any, List, Optional, Tuple

def load_env(env_path: Optional[str] = None):
    if env_path is None:
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        env_path = os.path.join(root_dir, ".env")
        if not os.path.exists(env_path):
            env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    
    if os.path.exists(env_path):
        try:
            with open(env_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        k, v = k.strip(), v.strip()
                        if k and not os.environ.get(k):
                            os.environ[k] = v.strip("'\"")
        except Exception:
            pass

load_env()

class Database:
    def __init__(
        self,
        db_type: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = None,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        sqlite_path: Optional[str] = None,
    ):
        self.db_type = (db_type or os.getenv("DB_TYPE", "postgresql")).lower()
        self.host = host or os.getenv("DB_HOST", "localhost")
        self.port = int(port or os.getenv("DB_PORT", "5432"))
        self.dbname = dbname or os.getenv("DB_NAME", "bibliotech")
        self.user = user or os.getenv("DB_USER", "postgres")
        self.password = password or os.getenv("DB_PASSWORD", "admin")
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.sqlite_path = sqlite_path or os.getenv("SQLITE_PATH", os.path.join(base_dir, "bibliotheque.db"))
        
        self.conn = None
        self.cur = None
        self.is_postgres = False
        self._connect()
        self._init_schema()

    def _connect(self):
        if self.db_type in ("postgres", "postgresql"):
            try:
                import psycopg2
                self.conn = psycopg2.connect(
                    host=self.host,
                    port=self.port,
                    dbname=self.dbname,
                    user=self.user,
                    password=self.password,
                    connect_timeout=3
                )
                self.cur = self.conn.cursor()
                self.is_postgres = True
                return
            except Exception as e:
                print(f"[DB Notice] Could not connect to PostgreSQL ({e}). Using SQLite fallback.")
                self.db_type = "sqlite"

        import sqlite3
        self.conn = sqlite3.connect(self.sqlite_path)
        self.cur = self.conn.cursor()
        self.is_postgres = False

    def _init_schema(self):
        if self.is_postgres:
            schema_sql = [
                """
                CREATE TABLE IF NOT EXISTS livre (
                    isbn VARCHAR(30) NOT NULL,
                    titre VARCHAR(255) NOT NULL,
                    auteur VARCHAR(255) NOT NULL,
                    editeur VARCHAR(255),
                    idlivre SERIAL PRIMARY KEY,
                    couv TEXT,
                    categorie VARCHAR(100)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS adherent (
                    identifiant SERIAL PRIMARY KEY,
                    nomAdherent VARCHAR(255) NOT NULL,
                    prenomAdherent VARCHAR(255) NOT NULL,
                    Mail VARCHAR(255),
                    telephone VARCHAR(30)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS emprunt (
                    NumLivre VARCHAR(50),
                    NomLivre VARCHAR(255),
                    DateEmprunt VARCHAR(30),
                    DateRetour VARCHAR(30),
                    NumEmprunt SERIAL PRIMARY KEY,
                    Identifiant INTEGER,
                    NomAdherent VARCHAR(255),
                    Auteur VARCHAR(255),
                    PrenomAdherent VARCHAR(255)
                );
                """
            ]
        else:
            schema_sql = [
                """
                CREATE TABLE IF NOT EXISTS livre (
                    isbn VARCHAR(30) NOT NULL,
                    titre VARCHAR(255) NOT NULL,
                    auteur VARCHAR(255) NOT NULL,
                    editeur VARCHAR(255),
                    idlivre INTEGER PRIMARY KEY AUTOINCREMENT,
                    couv TEXT,
                    categorie VARCHAR(100)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS adherent (
                    identifiant INTEGER PRIMARY KEY AUTOINCREMENT,
                    nomAdherent VARCHAR(255) NOT NULL,
                    prenomAdherent VARCHAR(255) NOT NULL,
                    Mail VARCHAR(255),
                    telephone VARCHAR(30)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS emprunt (
                    NumLivre VARCHAR(50),
                    NomLivre VARCHAR(255),
                    DateEmprunt VARCHAR(30),
                    DateRetour VARCHAR(30),
                    NumEmprunt INTEGER PRIMARY KEY AUTOINCREMENT,
                    Identifiant INTEGER,
                    NomAdherent VARCHAR(255),
                    Auteur VARCHAR(255),
                    PrenomAdherent VARCHAR(255)
                );
                """
            ]

        for stmt in schema_sql:
            self.cur.execute(stmt)
        self.conn.commit()

    def _normalize_query(self, query: str) -> str:
        if self.is_postgres:
            query = query.replace("?", "%s")
            query = query.replace("DATE('now')", "CURRENT_DATE")
            query = query.replace("date('now')", "CURRENT_DATE")
            query = query.replace("COLLATE NOCASE", "")
        else:
            query = query.replace("CURRENT_DATE", "DATE('now')")
        return query

    def execute(self, query: str, params: Optional[Tuple[Any, ...]] = None):
        query = self._normalize_query(query)
        if params is not None:
            self.cur.execute(query, params)
        else:
            self.cur.execute(query)
        return self.cur

    def fetchall(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> List[Tuple]:
        self.execute(query, params)
        return self.cur.fetchall()

    def fetchone(self, query: str, params: Optional[Tuple[Any, ...]] = None) -> Optional[Tuple]:
        self.execute(query, params)
        return self.cur.fetchone()

    def commit(self):
        if self.conn:
            self.conn.commit()

    def close(self):
        try:
            if self.cur:
                self.cur.close()
            if self.conn:
                self.conn.close()
        except Exception:
            pass

def get_db(sqlite_path: Optional[str] = None) -> Database:
    return Database(sqlite_path=sqlite_path)
