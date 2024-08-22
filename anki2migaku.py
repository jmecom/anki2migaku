import csv
import sqlite3
import shutil

from pathlib import Path
from dataclasses import dataclass

ANKI_DB_PATH = Path("/Users/jm/Library/Application Support/Anki2/User 1/collection.anki2")
DECK_ID = 1683426698762

def get_known_words():
    db_path = Path(ANKI_DB_PATH)

    # Create a copy of the database to work with
    db_copy_path = db_path.with_suffix('.copy.anki2')
    shutil.copy(db_path, db_copy_path)

    # Connect to the copied database
    conn = sqlite3.connect(db_copy_path)
    cursor = conn.cursor()

    # Query to get note, card information, and review count for cards in the specified deck
    query = """
    SELECT
        cards.id,
        notes.flds,
        cards.reps   -- Number of reviews
    FROM cards
    JOIN notes ON cards.nid = notes.id
    WHERE cards.reps > 0 AND cards.did = ?;  -- Only select cards that have been reviewed at least once and belong to the specified deck
    """

    cursor.execute(query, (DECK_ID,))
    rows = cursor.fetchall()
    conn.close()

    known_words = []
    for row in rows:
        card_id, fields, reps = row
        fields = fields.split('\x1f')  # Anki fields are separated by 0x1f character
        fields_str = "\t".join(fields)
        if fields[3] == "Vocabulary":
            known_words.append(fields[2])

    return known_words


if __name__ == "__main__":
    known_words = get_known_words()
    print(",".join(known_words))
