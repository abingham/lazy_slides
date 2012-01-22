import unittest

from lazy_slides.cache import Cache

from lazy_slides.tests.util import (remove, temp_file)

class CacheTest(unittest.TestCase):

    def setUp(self):
        self.db_file = 'test.db'
        remove(self.db_file)

    def tearDown(self):
        remove(self.db_file)

    def test_get(self):
        tag = 'tag'
        filename = 'test_file'

        cache = Cache(self.db_file)
        self.assertEqual(cache.get(tag), None)

        with temp_file(filename):
            cache.set(tag, filename)

            self.assertEqual(cache.get(tag), filename)

    def test_get_missing_file(self):
        tag = 'tag'
        filename = 'test_file'

        cache = Cache(self.db_file)

        with temp_file(filename):
            cache.set(tag, filename)

            self.assertEqual(cache.get(tag), filename)

        self.assertEqual(cache.get(tag), None)
