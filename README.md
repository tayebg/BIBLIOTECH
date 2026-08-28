# BIBLIOTECH

A desktop library management system featuring automatic ISBN bibliographic metadata fetching, book cataloging, subscriber management, loan and return tracking, overdue alerts, and contactless NFC/RFID badge support.

## Features

- **Book Catalog Management**: Add books by ISBN with automatic metadata retrieval (title, author, publisher, category) via `isbnlib`.
- **Subscriber Directory**: Register and manage library members with unique identification numbers, contact information, and search capability.
- **Loan & Return Tracking**: Issue book loans with automated return date calculations (30 days default) and process returns.
- **Overdue Tracking**: Dedicated filter and visual indicators for identifying overdue loans.
- **Hardware Integration**: Dual mode support—standard desktop mode and contactless NFC/RFID card reader mode (`pyscard` / ACR122U).
- **Flexible Database Backend**: PostgreSQL as the primary database with automatic fallback to embedded SQLite3.

## Tech Stack

- **Language**: Python 3.9+
- **GUI Framework**: CustomTkinter
- **Databases**: PostgreSQL (primary) / SQLite3 (embedded fallback)
- **Database Driver**: `psycopg2-binary`
- **Metadata Fetching**: `isbnlib`
- **Image Processing**: Pillow (PIL)
- **Smartcard / NFC**: `pyscard`
- **Testing**: `pytest`

## Project Structure

```
BIBLIOTECH/
├── img_readme/              # Interface screenshots and assets
├── sources/
│   ├── Annexe/
│   │   ├── font/            # Outfit typography files
│   │   ├── icones/          # UI icons
│   │   └── requirements.txt # Dependency list
│   ├── nfc/                 # ACR122U NFC reader drivers and utilities
│   ├── db.py                # Database abstraction layer (PostgreSQL & SQLite)
│   ├── migrate.py           # Data migration utility (SQLite -> PostgreSQL)
│   ├── BIBLIOTECH.py        # Standard desktop application
│   ├── BIBLIOTECH_nfc.py    # Contactless NFC hardware application
│   ├── bibliotheque.db      # SQLite database (standard mode)
│   └── bibliotheque_nfc.db  # SQLite database (NFC mode)
├── tests/
│   ├── test_database.py     # Database schema, CRUD, search, and overdue tests
│   └── test_logic.py        # Business logic and formatting tests
├── .env.example             # Database configuration template
├── .gitignore
├── requirements.txt         # Root package requirements
└── README.md
```

## Requirements

- Python 3.9 or higher
- PostgreSQL (optional, recommended for production/multi-user) or SQLite (built-in fallback)
- ACR122U NFC / RFID reader (optional, only required when running `BIBLIOTECH_nfc.py`)

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/tayebg/BIBLIOTECH.git
cd BIBLIOTECH
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

## Environment Variables & PostgreSQL Setup

Copy `.env.example` to `.env` in the project root:
```bash
cp .env.example .env
```

Configure your database connection in `.env`:
```ini
# Options: postgresql or sqlite
DB_TYPE=postgresql

# PostgreSQL Configuration
DB_HOST=localhost
DB_PORT=5432
DB_NAME=bibliotech
DB_USER=postgres
DB_PASSWORD=your_password_here

# SQLite Fallback Configuration
SQLITE_PATH=bibliotheque.db
```

### Creating the PostgreSQL Database
If using PostgreSQL, create the database before running:
```sql
CREATE DATABASE bibliotech;
```
The application will automatically initialize all required tables on startup.

### Migrating Existing Data from SQLite to PostgreSQL
To migrate sample data from the existing SQLite database into PostgreSQL:
```bash
python sources/migrate.py
```

## How to Run

### Standard Desktop Mode (No special hardware required)
```bash
python sources/BIBLIOTECH.py
```

### Contactless NFC Hardware Mode (Requires ACR122U Reader)
```bash
python sources/BIBLIOTECH_nfc.py
```

## Running Tests

Run the automated test suite using `pytest`:
```bash
pytest -v
```

## Basic Usage

1. **Adding Books**: Open the **LIVRE** tab, enter the book's ISBN and category, then click **AJOUTER**. A modal confirmation dialog will appear with pre-filled metadata fetched from online bibliographic registries.
2. **Adding Members**: Open the **ADHERENT** tab, enter the member's details (name, email, phone), and click **AJOUTER**.
3. **Borrowing Books**: In the **EMPRUNT** tab, enter the book ISBN / ID and member ID, then click **AJOUTER**.
4. **Returning Books**: In the **EMPRUNT** tab, enter the book and member details, then click **RETOUR**.
5. **Checking Overdue Books**: In the **EMPRUNT** tab, click **Livres en retard** to view books past their 30-day return window.

## Author

- **Tayeb Bekkouche** ([@tayebg](https://github.com/tayebg))
- Contact: tayebekk2004@gmail.com
- Repository: [https://github.com/tayebg/BIBLIOTECH](https://github.com/tayebg/BIBLIOTECH)
