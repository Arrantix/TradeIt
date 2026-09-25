import sqlite3
import unittest

from catalog import CardCatalog


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.catalog = CardCatalog()

    def test_original_catalog_is_complete_and_searchable(self):
        cards = self.catalog.search()
        self.assertEqual(len(cards), 102)
        first = cards[0]
        self.assertIn(first, self.catalog.search(first["name"]))
        self.assertIn(first, self.catalog.search(first["number"]))
        self.assertIn(first["card_type"], self.catalog.types())

    def test_search_input_is_data_and_catalog_is_read_only(self):
        self.assertEqual(self.catalog.search("' OR 1=1 --"), [])
        self.assertRaises(ValueError, self.catalog.search, "x" * 121)
        with self.catalog._connect() as db:
            with self.assertRaises(sqlite3.OperationalError):
                db.execute("DELETE FROM base_set_cards")
        self.assertEqual(len(self.catalog.search()), 102)


if __name__ == "__main__":
    unittest.main()
