import unittest

from lazy_slides.cache import open_cache

from lazy_slides.tests.util import (remove, temp_file)

class CacheTest(unittest.TestCase):

    def setUp(self):
        self.db_file = ':memory:'
    #     remove(self.db_file)

    # def tearDown(self):
    #     remove(self.db_file)

    def test_get(self):
        tag = 'tag'
        filename = 'test_file'

        with open_cache(self.db_file, 1000) as cache:
            self.assertEqual(cache.get(tag), None)

            with temp_file(filename):
                cache.set(tag, filename)

                self.assertEqual(cache.get(tag), filename)

    def test_get_missing_file(self):
        tag = 'tag'
        filename = 'test_file'

        with open_cache(self.db_file, 100) as cache:

            with temp_file(filename):
                cache.set(tag, filename)

                self.assertEqual(cache.get(tag), filename)

            self.assertEqual(cache.get(tag), None)

    def test_size(self):
        with open_cache(self.db_file, 1000) as cache:
            self.assertEqual(cache.size(), 0)

            for i in range(100):
                cache.set(str(i), str(i))
                self.assertEqual(cache.size(), i + 1)

    def test_trim(self):
        SIZE = 100

        with open_cache(self.db_file, 1000) as cache:
            for i in range(SIZE):
                cache.set(str(i), str(i))

            self.assertEqual(cache.size(), SIZE)

            NEW_SIZE=40
            cache.trim(NEW_SIZE)
            self.assertEqual(cache.size(), NEW_SIZE)

            cache.trim(cache.size() + 1)
            self.assertEqual(cache.size(), NEW_SIZE)
