"""Read-only access to the course project's original card catalogue."""

from contextlib import closing
from pathlib import Path
import sqlite3


DEFAULT_DB = Path(__file__).with_name("pokemon_base_set.db")


class CardCatalog:
    def __init__(self, db_path=DEFAULT_DB):
        self.db_path = Path(db_path)
        if not self.db_path.is_file():
            raise FileNotFoundError(f"Card catalogue missing: {self.db_path}")

    def _connect(self):
        db = sqlite3.connect(self.db_path.resolve().as_uri() + "?mode=ro", uri=True)
        db.row_factory = sqlite3.Row
        return db

    def types(self):
        with closing(self._connect()) as db:
            return [row[0] for row in db.execute(
                "SELECT DISTINCT card_type FROM base_set_cards ORDER BY card_type"
            )]

    def search(self, term="", card_type=""):
        term = term.strip()
        if len(term) > 120:
            raise ValueError("Search term is too long")
        with closing(self._connect()) as db:
            rows = db.execute(
                "SELECT id, name, number, rarity, condition, card_type, is_holo, notes "
                "FROM base_set_cards "
                "WHERE (? = '' OR instr(lower(name), lower(?)) > 0 OR instr(number, ?) > 0) "
                "AND (? = '' OR card_type = ?) ORDER BY id",
                (term, term, term, card_type, card_type),
            ).fetchall()
        return [dict(row) for row in rows]
