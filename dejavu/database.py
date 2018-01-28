# coding: utf-8
from __future__ import absolute_import
from itertools import izip_longest

import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

from .utils import settings

db = SqliteExtDatabase(settings.DBNAME)


class Music(peewee.Model):
    name = peewee.CharField(256)
    fingerprinted = peewee.BooleanField(default=False)
    sha1 = peewee.BlobField()

    class Meta:
        database = db

    @classmethod
    def count(cls):
        return cls.filter(fingerprinted=True).count()

    @classmethod
    def exists(cls, **kws):
        return cls.filter(**kws).exists()

    def finish(self):
        self.fingerprinted = True
        self.save()


class Fingerprint(peewee.Model):
    hash = peewee.BlobField(index=True)
    music = peewee.ForeignKeyField(Music)
    offset = peewee.IntegerField()

    class Meta:
        database = db
        # 联合唯一
        indexes = [(('hash', 'music', 'offset'), True)]

    @classmethod
    def count(cls):
        return cls.select().count()


db.connect()
# https://github.com/coleifer/peewee/issues/211
Music.create_table(fail_silently=True)
Fingerprint.create_table(fail_silently=True)
Music.delete().filter(fingerprinted=False).execute()


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return (filter(None, values) for values
            in izip_longest(fillvalue=fillvalue, *args))


def insert_hashes(music, hashes):
    for hashes in grouper(hashes, 100):
        data = ({'hash': h, 'music': music, 'offset': offset} for h, offset in hashes)
        Fingerprint.insert_many(data).on_conflict(action='IGNORE').execute()


def return_matches(hashes):
    """
    Return the (song_id, offset_diff) tuples associated with
    a list of (sha1, sample_offset) values.
    """
    # Create a dictionary of hash => offset pairs for later lookups
    mapper = dict(hashes)

    for hashes in grouper(mapper.keys(), 100):
        for f in Fingerprint.filter(hash__in=hashes):
            yield f.music_id, f.offset - mapper[str(f.hash)]
