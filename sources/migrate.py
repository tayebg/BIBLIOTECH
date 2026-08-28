# -*- coding: utf-8 -*-
"""
Migration Utility: Migrate existing records from SQLite to PostgreSQL.
"""

import os
import sys
import sqlite3
import psycopg2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SQLITE_DB = os.path.join(BASE_DIR, "bibliotheque.db")

def migrate(
    host="localhost",
    port=5432,
    dbname="bibliotech",
    user="postgres",
    password="admin",
    sqlite_path=SQLITE_DB
):
    print(f"[*] Starting migration from SQLite ({sqlite_path}) -> PostgreSQL ({dbname}@{host}:{port})...")
    
    if not os.path.exists(sqlite_path):
        print(f"[!] SQLite file {sqlite_path} does not exist.")
        return False
    
    s_conn = sqlite3.connect(sqlite_path)
    s_cur = s_conn.cursor()
    
    try:
        p_conn = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password
        )
        p_conn.autocommit = True
        p_cur = p_conn.cursor()
    except Exception as e:
        print(f"[!] PostgreSQL Connection Failed: {e}")
        return False
    
    # Drop existing tables to recreate with proper column order
    p_cur.execute("DROP TABLE IF EXISTS emprunt CASCADE;")
    p_cur.execute("DROP TABLE IF EXISTS livre CASCADE;")
    p_cur.execute("DROP TABLE IF EXISTS adherent CASCADE;")

    schema = [
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
    for stmt in schema:
        p_cur.execute(stmt)
    
    s_cur.execute("SELECT isbn, titre, auteur, editeur, idlivre, couv, categorie FROM livre")
    livres = s_cur.fetchall()
    for row in livres:
        p_cur.execute(
            """
            INSERT INTO livre(isbn, titre, auteur, editeur, idlivre, couv, categorie)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (idlivre) DO UPDATE SET
                isbn=EXCLUDED.isbn, titre=EXCLUDED.titre, auteur=EXCLUDED.auteur,
                editeur=EXCLUDED.editeur, couv=EXCLUDED.couv, categorie=EXCLUDED.categorie
            """,
            row
        )
    print(f"[+] Migrated {len(livres)} records into table 'livre'.")

    s_cur.execute("SELECT identifiant, nomAdherent, prenomAdherent, Mail, telephone FROM adherent")
    adherents = s_cur.fetchall()
    for row in adherents:
        p_cur.execute(
            """
            INSERT INTO adherent(identifiant, nomAdherent, prenomAdherent, Mail, telephone)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (identifiant) DO UPDATE SET
                nomAdherent=EXCLUDED.nomAdherent, prenomAdherent=EXCLUDED.prenomAdherent,
                Mail=EXCLUDED.Mail, telephone=EXCLUDED.telephone
            """,
            row
        )
    print(f"[+] Migrated {len(adherents)} records into table 'adherent'.")

    s_cur.execute("SELECT NumLivre, NomLivre, DateEmprunt, DateRetour, NumEmprunt, Identifiant, NomAdherent, Auteur, PrenomAdherent FROM emprunt")
    emprunts = s_cur.fetchall()
    for row in emprunts:
        p_cur.execute(
            """
            INSERT INTO emprunt(NumLivre, NomLivre, DateEmprunt, DateRetour, NumEmprunt, Identifiant, NomAdherent, Auteur, PrenomAdherent)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (NumEmprunt) DO UPDATE SET
                NumLivre=EXCLUDED.NumLivre, NomLivre=EXCLUDED.NomLivre, DateEmprunt=EXCLUDED.DateEmprunt,
                DateRetour=EXCLUDED.DateRetour, Identifiant=EXCLUDED.Identifiant, NomAdherent=EXCLUDED.NomAdherent,
                Auteur=EXCLUDED.Auteur, PrenomAdherent=EXCLUDED.PrenomAdherent
            """,
            row
        )
    print(f"[+] Migrated {len(emprunts)} records into table 'emprunt'.")

    for tbl, col, pkey in [("livre", "idlivre", "livre_idlivre_seq"),
                           ("adherent", "identifiant", "adherent_identifiant_seq"),
                           ("emprunt", "NumEmprunt", "emprunt_numemprunt_seq")]:
        try:
            p_cur.execute(f"SELECT setval('{pkey}', COALESCE((SELECT MAX({col}) FROM {tbl}), 1));")
        except Exception:
            pass

    s_conn.close()
    p_conn.close()
    print("[*] Migration completed successfully!")
    return True

if __name__ == "__main__":
    migrate()
