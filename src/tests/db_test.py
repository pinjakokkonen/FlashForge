import unittest
from tests import db_helper
from modules import database
from config import app

class TestDatabase(unittest.TestCase):
    """Class for testing the database"""

    @classmethod
    def setUpClass(cls):
        cls.app = app
        cls.context = cls.app.app_context()

        with cls.context:
            db_helper.setup_db()

    def setUp(self):
        pass

    def tearDown(self):
        with self.context:
            db_helper.reset_db("articles")

    def test_database_add(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))

    def test_database_query(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            res = database.get_all_articles()
            expected = [(res[0].id, 'Author', 'Title', 'Journal', 2024)]
            self.assertEqual(res, expected)

    def test_database_add_duplicate(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            self.assertFalse(database.add_article('Author', 'Title', 'Journal', 2024))

    def test_database_valid_search(self):
        with self.context:
            expected = ('Author', 'Title', 'Journal', 2024)
            self.assertTrue(database.add_article(*expected))
            res = database.search_result('Au')
            self.assertEqual(res, [expected])
            res = database.search_result('thor')
            self.assertEqual(res, [expected])
            res = database.search_result('2024')
            self.assertEqual(res, [expected])

    def test_database_invalid_search(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            res = database.search_result('Invalid')
            self.assertEqual(res, [])
            res = database.search_result('1999')
            self.assertEqual(res, [])

    def test_database_edit_article(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            all_articles = database.get_all_articles()
            self.assertTrue(database.edit_article(all_articles[0].id, 'Author2', 'Title2', 'Journal2', 2022))
            expected = (all_articles[0].id, 'Author2', 'Title2', 'Journal2', 2022)
            res = database.article_from_id(all_articles[0].id)
            self.assertEqual(res, expected)

    def test_database_delete_article(self):
        with self.context:
            self.assertTrue(database.add_article('Author', 'Title', 'Journal', 2024))
            all_articles = database.get_all_articles()
            self.assertTrue(database.delete_article(all_articles[0].id))
            res = database.get_all_articles()
            self.assertEqual(res, [])
