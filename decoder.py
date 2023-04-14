import os
import numpy as np
from pydub import AudioSegment
from pydub.utils import audioop
import wavio
from hashlib import sha1
from six.moves import xrange


def unique_hash(filepath, blocksize=2 ** 20):
    """
    Inspired by MD5 version here: https://stackoverflow.com/a/1131255/712997
    """
    s = sha1()
    with open(filepath, "rb") as f:
        while True:
            buf = f.read(blocksize)
            if not buf:
                break
            s.update(buf)
    return s.hexdigest().upper()


def read(filename, limit=None):
    """
    Reads any file supported by pydub (ffmpeg) and returns the data contained
    within. If file reading fails due to input being a 24-bit wav file,
    wavio is used as a backup.

    Can be optionally limited to a certain amount of seconds from the start
    of the file by specifying the `limit` parameter. This is the amount of
    seconds from the start of the file.

    returns: (channels, sample rate)
    """
    # pydub does not support 24-bit wav files, use wavio when this occurs
    try:
        audiofile = AudioSegment.from_file(filename)

        if limit:
            audiofile = audiofile[:limit * 1000]

        data = np.fromstring(audiofile._data, np.int16)

        channels = []
        for chn in xrange(audiofile.channels):
            channels.append(data[chn::audiofile.channels])

    except audioop.error:
        fs, _, audiofile = wavio.readwav(filename)

        if limit:
            audiofile = audiofile[:limit * 1000]

        audiofile = audiofile.T
        audiofile = audiofile.astype(np.int16)

        channels = []
        for chn in audiofile:
            channels.append(chn)

    return channels, audiofile.frame_rate, unique_hash(filename)


def path_to_songname(path):
    """
    Extracts song name from a filepath.
    Used to identify which songs have already been fingerprinted on disk.
    """
    return os.path.splitext(os.path.basename(path))[0]
