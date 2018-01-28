# coding: utf-8
import os
import unittest

from . import audio
from . import utils
from .fingerprint import fingerprint


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestUtils(unittest.TestCase):

    def test_sha1(self):
        h = utils.sha1('text', 10)
        self.assertEqual(len(h), 10)
        h = utils.sha1((1, 3, 2), 10)
        self.assertEqual(len(h), 10)

    def test_sha1_file(self):
        h = utils.sha1_file(__file__)
        self.assertEqual(len(h), 20)


class TestMusic(unittest.TestCase):

    def test_from_file(self):
        path = 'mp3/Sean-Fournier--Falling-For-You.mp3'
        path = os.path.join(BASE_DIR, path)
        channels, sr = audio.from_file(path)


class TestFingerprint(unittest.TestCase):

    def test_fingerprint(self):
        path = 'mp3/Sean-Fournier--Falling-For-You.mp3'
        path = os.path.join(BASE_DIR, path)
        channels, sr = audio.from_file(path)
        for channel in channels:
            fingerprint(channel, sr)


class TestDatabase(unittest.TestCase):

    def setUp(self):
        utils.settings.DBNAME = ':memory:'
        import database
        reload(database)    # for reopen an empty database
        self.db = database

    def test_music(self):
        h = '01234567890123456789'
        self.assertFalse(self.db.Music.exists(sha1=h))
        music = self.db.Music.create(name='name', sha1=h)
        self.assertTrue(self.db.Music.exists(sha1=h))
        # 没有完成的提取指纹的音频不被计入
        self.assertEqual(self.db.Music.count(), 0)
        music.finish()
        self.assertEqual(self.db.Music.count(), 1)

    def test_fingerprint(self):
        h = '01234567890123456789'
        music = self.db.Music.create(name='name', sha1='01234567890123456789')
        # 相同的指纹会被数据库去重
        self.db.insert_hashes(music, [(h, 2), (h, 2)])
        self.assertEqual(self.db.Fingerprint.count(), 1)
        self.db.return_matches([h])
