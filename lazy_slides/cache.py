import contextlib
import logging
import os
import sqlite3
import time


log = logging.getLogger(__name__)

cache_table_def = '''
create table
if not exists
cache (
tag text primary key unique,
filename text,
timestamp real)
'''

get_query = 'SELECT filename FROM cache WHERE tag=?'

set_query = 'INSERT INTO cache VALUES (?,?,?)'

delete_query = 'DELETE FROM cache WHERE tag=?'

trim_query = '''
DELETE FROM cache
WHERE tag NOT IN (
  SELECT tag
  FROM (
    SELECT tag
    FROM cache
    ORDER BY timestamp DESC
    LIMIT ?
  )
)
'''

class Cache:
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        cur = self.conn.cursor()
        cur.execute(cache_table_def)

    def get(self, tag):
        log.info('retrieving from cache: {}'.format(tag))

        cur = self.conn.cursor()
        cur.execute(get_query, (tag,))
        row = cur.fetchone()

        # If no results, just return None
        if not row:
            log.info('Cache miss: {}'.format(tag))
            return None

        filename = row[0]

        log.info('Cache hit: {} -> {}'.format(tag, filename))

        # Otherwise, ensure that the file exists.
        if not os.path.exists(filename):
            log.info('Cache hit for missing file: {} -> {}'.format(tag, filename))
            cur.execute(delete_query, (tag,))
            return None

        return filename

    def set(self, tag, filename):
        log.info('Cache set: {} -> {}'.format(tag, filename))
        cur = self.conn.cursor()
        cur.execute(set_query, (tag, filename, time.time()))

    def trim(self, size):
        log.info('Cache trim: {}'.format(size))
        cur = self.conn.cursor()
        cur.execute(trim_query, (size,))

    def close(self):
        log.info('Closing cache')
        self.conn.commit()
        self.conn.close()

@contextlib.contextmanager
def open_cache(filename, size):
    cache = Cache(filename)

    try:
        yield cache
        cache.trim(size)
    finally:
        cache.close()
