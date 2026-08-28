import os
import sys
import pytest

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sources_dir = os.path.join(base_dir, "sources")
if sources_dir not in sys.path:
    sys.path.insert(0, sources_dir)

from db import Database

@pytest.fixture
def sqlite_db(tmp_path):
    db_file = str(tmp_path / "test.db")
    db = Database(db_type="sqlite", sqlite_path=db_file)
    yield db
    db.close()

def test_database_initialization(sqlite_db):
    tables = [r[0] for r in sqlite_db.fetchall("SELECT name FROM sqlite_master WHERE type='table'")]
    assert "livre" in tables
    assert "adherent" in tables
    assert "emprunt" in tables

def test_crud_livre(sqlite_db):
    sqlite_db.execute(
        "INSERT INTO livre(isbn, titre, auteur, editeur, categorie) VALUES (?, ?, ?, ?, ?)",
        ("9782070360024", "L'Etranger", "Albert Camus", "Gallimard", "Roman")
    )
    sqlite_db.commit()
    
    row = sqlite_db.fetchone("SELECT * FROM livre WHERE isbn=?", ("9782070360024",))
    assert row is not None
    assert row[1] == "L'Etranger"
    assert row[2] == "Albert Camus"

def test_crud_adherent(sqlite_db):
    sqlite_db.execute(
        "INSERT INTO adherent(nomAdherent, prenomAdherent, Mail, telephone) VALUES (?, ?, ?, ?)",
        ("Dupont", "Jean", "jean.dupont@test.com", "0601020304")
    )
    sqlite_db.commit()
    
    row = sqlite_db.fetchone("SELECT * FROM adherent WHERE nomAdherent=?", ("Dupont",))
    assert row is not None
    assert row[1] == "Dupont"
    assert row[2] == "Jean"

def test_emprunt_and_overdue(sqlite_db):
    sqlite_db.execute(
        "INSERT INTO emprunt(NumLivre, NomLivre, DateEmprunt, DateRetour, Identifiant, NomAdherent, Auteur, PrenomAdherent) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        ("1", "L'Etranger", "2026-01-01", "2026-02-01", 1, "Dupont", "Albert Camus", "Jean")
    )
    sqlite_db.commit()
    
    loans = sqlite_db.fetchall("SELECT * FROM emprunt WHERE DATE(DateRetour) < CURRENT_DATE")
    assert len(loans) >= 1
    # Index 1 is NomLivre
    assert loans[0][1] == "L'Etranger"

def test_search_filters(sqlite_db):
    sqlite_db.execute(
        "INSERT INTO livre(isbn, titre, auteur, editeur, categorie) VALUES (?, ?, ?, ?, ?)",
        ("1234567890", "Python Programming", "Guido van Rossum", "O'Reilly", "Tech")
    )
    sqlite_db.commit()
    
    results = sqlite_db.fetchall("SELECT * FROM livre WHERE titre LIKE ?", ("%Python%",))
    assert len(results) == 1
    assert results[0][1] == "Python Programming"

def test_postgresql_connection():
    try:
        pg_db = Database(
            db_type="postgresql",
            host="localhost",
            port=5432,
            dbname="bibliotech",
            user="postgres",
            password="admin"
        )
        if pg_db.is_postgres:
            res = pg_db.fetchall("SELECT COUNT(*) FROM livre")
            assert len(res) >= 1
            pg_db.close()
    except Exception:
        pytest.skip("Local PostgreSQL not available or not running.")
