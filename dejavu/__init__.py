from . import audio
from . import database
from . import utils
from .fingerprint import fingerprint
from .recognize import recognize


def fingerprint_file(fn, music_name=None, duration=None):
    # don't refingerprint already fingerprinted files
    h = utils.sha1_file(fn)
    if not database.Music.exists(sha1=h):
        music_name = music_name or utils.path_to_name(fn)
        music = database.Music.create(name=music_name, sha1=h)

        channels, sr = audio.from_file(fn, duration=duration)
        hashes = set()
        for channel in channels:
            t = fingerprint(channel, sr=sr)
            hashes |= set(t)

        database.insert_hashes(music, hashes)
        music.finish()


def recognize_fine(fn):
    y, sr = audio.from_file(fn)
    return recognize(y, sr)
