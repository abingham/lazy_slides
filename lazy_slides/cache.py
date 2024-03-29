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

    engine = Column(String, primary_key=True)
    tag = Column(String, primary_key=True)
    width = Column(Integer, primary_key=True)
    height = Column(Integer, primary_key=True)
    filename = Column(String)
    timestamp = Column(DateTime)

    def __init__(self,
                 engine,
                 tag,
                 width,
                 height,
                 filename,
                 timestamp=None):
        self.engine = engine
        self.tag = tag
        self.width = width
        self.height = height
        self.filename = filename
        if timestamp:
            self.timestamp = timestamp
        else:
            self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return '<Entry(engine="{}", tag="{}", width="{}", height="{}", filename="{}", timestamp={})>'.format(
            self.engine,
            self.tag,
            self.width,
            self.height,
            self.filename,
            self.timestamp)

log = logging.getLogger(__name__)

class Cache:
    def __init__(self, filename):
        self.engine = sqlalchemy.create_engine(
            'sqlite:///{}?check_same_thread=False'.format(filename))


        Base.metadata.create_all(self.engine)

        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def _get_entry(self, engine, tag, width, height):
        return self.session.query(Entry).filter_by(tag=tag,
                                                   engine=engine,
                                                   width=width,
                                                   height=height).first()

    def get(self, engine, tag, width=-1, height=-1):
        log.info('retrieving from cache: {} {} {} {}'.format(
            engine, tag, width, height))

        entry = self._get_entry(engine, tag, width, height)
        if not entry:
            log.info('cache miss: {} {} {} {}'.format(
                engine, tag, width, height))
            return None

        log.info('cache hit: {} {} {} {}'.format(
            engine, tag, width, height))

        # Don't report a cache hit unless the file exists.
        if not os.path.exists(entry.filename):
            log.info('cache file missing: {} {} {} {}'.format(
                engine, tag, width, height))
            # If the file doesn't exist, remove the cache entry.
            self.session.delete(entry)
            return None

        return entry.filename

    def set(self, engine, tag, filename, width=-1, height=-1):
        log.info('Cache set: {} {} {} {} -> {}'.format(
            engine, tag, width, height, filename))

        e = self._get_entry(engine, tag, width, height)
        if e:
            e.filename = filename
            e.timestamp = datetime.datetime.now()
        else:
            e = Entry(engine=engine,
                      tag=tag,
                      filename=filename,
                      width=width,
                      height=height)
            self.session.add(e)

    def trim(self, size):
        log.info('Cache trim: {}'.format(size))

        curr_size = self.size()
        if curr_size <= size:
            return

        # TODO: There's probably a way to speed this up which avoids a
        # count + a series of deletions. Perhaps a subquery...look
        # into it.
        query = self.session.query(Entry).order_by(Entry.timestamp).limit(curr_size - size)
        for entry in query:
            self.session.delete(entry)

    def size(self):
        return self.session.query(Entry).count()

    def close(self, commit=True):
        log.info('Closing cache')
        if commit:
            self.session.commit()

@contextlib.contextmanager
def open_cache(filename, size):
    cache = Cache(filename)

    try:
        yield cache
        cache.trim(size)
        cache.close()
    except Exception:
        cache.close(commit=False)
        raise
