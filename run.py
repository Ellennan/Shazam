from dejavu import Dejavu
from recognize import FileRecognizer
import os

config = {
    "database": {
        "host": "127.0.0.1",
        "user": "root",
        "passwd": "ellenndy",
        "db": "genre",
    },
    "database_type": "mysql",
    # "fingerprint_limit": 20
}

djv = Dejavu(config)


def fingerprint(f):
    return djv.fingerprint_file(f)


def find(f):
    djv.config['fingerprint_limit'] = 20
    return djv.recognize(FileRecognizer, f)
    # song = djv.recognize(FileRecognizer, f)
    # filename = os.path.basename(f).rsplit(".", 1)[0]
    # songname = filename.split("_")[0]
    # if song is not None:
    #     return ("Actual:" + filename
    #             + "\tPredicted:" + song['song_name']
    #             + "\tConfidence:" + str(song['confidence'])
    #             + "\tCorrectness:" + str(song['song_name'] == songname))
    # else:
    #     return "Actual: " + filename + "\t\t" + "Predicted: " + song + "\tFalse"


def database():
    return djv.db.get_songs()
