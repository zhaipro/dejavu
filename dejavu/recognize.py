import time
from collections import Counter

from . import database
from . import fingerprint


def align_matches(matches):
    """
        Finds hash matches that align in time with other matches and finds
        consensus about which hashes are "true" signal from the audio.

        Returns a dictionary with match information.
    """
    # align by diffs
    counter = Counter(matches)
    (mid, largest), largest_count = counter.most_common(1)[0]
    # extract idenfication
    music = database.Music.get(id=mid)

    # return match info
    nseconds = round(float(largest) / 86.835, 5)
    music = {
        'music': {
            'id': music.id,
            'name': music.name,
            'sha1': str(music.sha1),
        },
        'confidence': largest_count,
        'offset': int(largest),
        'offset_seconds': nseconds,
    }
    return music


def recognize(channels, sr):
    t = time.time()
    matches = []
    for samples in channels:
        hashes = fingerprint(samples, sr=sr)
        d = database.return_matches(hashes)
        matches.extend(d)
    match = align_matches(matches)
    if match:
        match['match_time'] = time.time() - t
    return match
