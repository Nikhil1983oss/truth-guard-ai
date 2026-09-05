import sqlite3
import json
from datetime import datetime
import os


# ============================================================
# DATABASE CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

DATABASE_PATH = os.path.join(
    DATABASE_DIR,
    "truthguard.db"
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    connection = sqlite3.connect(
        DATABASE_PATH
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# INITIALIZE DATABASE
# ============================================================

def init_database():

    os.makedirs(
        DATABASE_DIR,
        exist_ok=True
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS analyses (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            file_id TEXT UNIQUE NOT NULL,

            filename TEXT NOT NULL,

            media_type TEXT,

            verdict TEXT,

            fake_score REAL,

            real_score REAL,

            risk_score REAL,

            risk_level TEXT,

            analysis_json TEXT,

            created_at TEXT NOT NULL

        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAVE ANALYSIS
# ============================================================

def save_analysis(
    file_id,
    filename,
    media_type,
    analysis
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO analyses (

            file_id,
            filename,
            media_type,
            verdict,
            fake_score,
            real_score,
            risk_score,
            risk_level,
            analysis_json,
            created_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (
            file_id,

            filename,

            media_type,

            analysis.get("verdict"),

            analysis.get("fake_score"),

            analysis.get("real_score"),

            analysis.get("risk_score"),

            analysis.get("risk_level"),

            json.dumps(
                analysis
            ),

            datetime.now().isoformat(
                timespec="seconds"
            )
        )
    )

    connection.commit()

    connection.close()


# ============================================================
# GET ALL HISTORY
# ============================================================

def get_history():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT

            id,
            file_id,
            filename,
            media_type,
            verdict,
            fake_score,
            real_score,
            risk_score,
            risk_level,
            created_at

        FROM analyses

        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [
        dict(row)
        for row in rows
    ]


# ============================================================
# GET ONE ANALYSIS
# ============================================================

def get_analysis(
    file_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM analyses

        WHERE file_id = ?
        """,

        (file_id,)
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:
        return None

    data = dict(row)

    if data.get("analysis_json"):

        data["analysis"] = json.loads(
            data["analysis_json"]
        )

    return data


# ============================================================
# DELETE ANALYSIS
# ============================================================

def delete_analysis(
    file_id
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM analyses

        WHERE file_id = ?
        """,

        (file_id,)
    )

    connection.commit()

    deleted = cursor.rowcount

    connection.close()

    return deleted