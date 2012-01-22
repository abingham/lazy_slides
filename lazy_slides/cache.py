import contextlib
import datetime
import logging
import os

import sqlalchemy
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'

    tag = Column(String, primary_key=True)
    filename = Column(String)
    timestamp = Column(DateTime)

    def __init__(self, tag, filename, timestamp=None):
        self.tag = tag
        self.filename = filename
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<Entry("{}", "{}", {})>'.format(
            self.tag,
            self.filename,
            self.timestamp)

log = logging.getLogger(__name__)

class Cache:
    def __init__(self, filename):
        self.engine = sqlalchemy.create_engine('sqlite:///{}'.format(filename))

        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def get(self, tag):
        log.info('retrieving from cache: {}'.format(tag))

        entry = self.session.query(Entry).filter_by(tag=tag).first()
        if not entry:
            return None

        # Don't report a cache hit unless the file exists.
        if not os.path.exists(entry.filename):
            # If the filex doesn't exist, remove the cache entry.
            self.session.delete(entry)
            return None

        return entry.filename

    def set(self, tag, filename):
        log.info('Cache set: {} -> {}'.format(tag, filename))
        e = Entry(tag=tag,
                  filename=filename)
        self.session.add(e)

    def trim(self, size):
        log.info('Cache trim: {}'.format(size))

        curr_size = self.size()
        if curr_size <= size:
            return

        query = self.session.query(Entry).order_by(Entry.timestamp).limit(curr_size - size)
        for entry in query:
            self.session.delete(entry)

    def size(self):
        return self.session.query(Entry).count()

    def close(self):
        log.info('Closing cache')
        self.session.commit()

@contextlib.contextmanager
def open_cache(filename, size):
    cache = Cache(filename)

    try:
        yield cache
        cache.trim(size)
    finally:
        cache.close()
