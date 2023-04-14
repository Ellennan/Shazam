import mysql.connector
from dejavu import Dejavu
from recognize import FileRecognizer
import decoder
import fingerprint
import os
import glob
import librosa
import librosa.display
import soundfile as sf
from pydub import AudioSegment
from scipy import signal
from pitch import pitch_shift
from timbre import filter
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)


def trans_mp3_to_wav(filepath):
    song = AudioSegment.from_file(filepath)
    filename = os.path.basename(filepath).split(".")[0]
    songname = os.path.split(filepath)[0].split("\\")[1]
    path = "wav/" + songname
    if not os.path.exists(path):
        os.makedirs(path)
        song.export("wav/" + songname + "/" + filename + ".wav", format="wav")


# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="ellenndy"
# )
#
# mycursor = mydb.cursor()
#
# mycursor.execute("DROP DATABASE test")
# mycursor.execute("CREATE DATABASE IF NOT EXISTS test")


config = {
    "database": {
        "host": "127.0.0.1",
        "user": "root",
        "passwd": "ellenndy",
        "db": "dejavu",
    },
    "database_type": "mysql",
    # "fingerprint_limit": 10
}

djv = Dejavu(config)

if __name__ == '__main__':
    # for file in glob.glob("wav_part/*/*.wav"):
    #     djv.fingerprint_file(file, os.path.split(file)[0].split("\\")[1])
    # djv.fingerprint_file("wav/Let_It_Be/beatles+1+26-Let_It_Be.wav")
    # djv.fingerprint_directory("Genre/*/*.wav")

    # print(djv.db.get_num_fingerprints())

    # for file in glob.glob("coversongs/covers32k/*/*.mp3"):
    #     trans_mp3_to_wav(file)
    # for file in glob.glob("wav_part/*/*.wav"):
    #     pitch_shift(file)
    # for file in glob.glob("Genres_timbre/*/*.wav"):
    #     filter(file, gain1=0, gain2=0, gain3=0)
    #     filter(file, gain4=0, gain5=0, gain6=0)
    #     filter(file, gain7=0, gain8=0, gain9=0)

    # 识别文件
    # TP = 0
    # TN = 0
    # FP = 0
    # FN = 0
    # for file in glob.glob("testing/pitch/*/*.wav"):
    #     print(file)
    #     file_index = int(os.path.basename(file).split(".")[1].split("_")[0])
    #     filename = os.path.basename(file).rsplit(".", 1)[0]
    #     songname = filename.split("_")[0]
    #
    #     if file_index < 6:
    #         song = djv.recognize(FileRecognizer, file)
    #         print(song)
    #
    #     if file_index < 6:
    #         if song is None:
    #             FN += 1
    #         elif song['song_name'] == songname:
    #             TP += 1
    #         else:
    #             FP += 1
    #     # else:
    #     #     if song is None:
    #     #         TN += 1
    #     #     else:
    #     #         FP += 1
    # print(TP)
    # print(TN)
    # print(FP)
    # print(FN)

    # for file in glob.glob("wav_part/*/*.wav"):
    #     channels, Fs, file_hash = decoder.read(file, 10)
    #     print(Fs)

    # waveform after pitch shift and timbre change
    # count = 0
    # for file in glob.glob("wav/Let_It_Be/*.wav"):
    #     count += 1
    #     y, sr = librosa.load(file)
    #     print(len(y))
    #     y = y[10000:100000]
    #     ax = plt.subplot(10, 1, count)
    #     ax.set_title(file, fontsize=10)
    #     # ax.set_xlabel('xlabel', fontsize=10)  # xlabel
    #     # ax.set_ylabel('ylabel', fontsize=10)  # ylabel
    #     ax.plot(y)
    # plt.savefig('result.png')
    # plt.show()

    # spectrogram of different pitch and timbre
    # count = 0
    # for file in glob.glob("wav/Let_It_Be/*.wav"):
    #     count += 1
    #     y, sr = librosa.load(file)
    #     y = y[10000:100000]
    #     y = librosa.stft(y)
    #     db = librosa.amplitude_to_db(abs(y))
    #     plt.figure()
    #     plt.title(file)
    #     librosa.display.specshow(db, sr=sr, x_axis='time', y_axis='log')
    #     plt.colorbar()
    #     plt.savefig('result' + str(count) + '.png')
    #     plt.show()

    # Peak
    # arr2D = np.array([(0, 0, 0, 0, 1, 1),
    #                   (0, 0, 0, 0, 2, 2),
    #                   (0, 0, 0, 0, 1, 1),
    #                   (3, 3, 3, 0, 3, 3),
    #                   (1, 1, 1, 0, 1, 1)])
    # struct = generate_binary_structure(2, 1)
    # print('struct:')
    # print(struct)
    # neighborhood = iterate_structure(struct, 1)
    # print('neighborhood:')
    # print(neighborhood)
    #
    # # find local maxima using our filter shape
    # local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    # print('local_max:')
    # print(local_max)
    # background = (arr2D == 0)
    # print('background:')
    # print(background)
    # eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)
    # print('eroded_background:')
    # print(eroded_background)
    #
    # # Boolean mask of arr2D with True at peaks
    # detected_peaks = local_max ^ eroded_background
    # print('detected_peaks:')
    # print(detected_peaks)
    #
    # # extract peaks
    # amps = arr2D[detected_peaks]
    # print(amps)
    # j, i = np.where(detected_peaks)
    # print(j)
    # print(i)

    # for file in glob.glob("wav/Yesterday/*.wav"):
    #     channels, Fs, file_hash = decoder.read(file, 10)
    #     channel_amount = len(channels)
    #     for channeln, channel in enumerate(channels):
    #         print("Fingerprinting channel %d/%d for %s" % (channeln + 1, channel_amount, file))
    #         # print("Fs: {}".format(Fs))
    #         hashes = fingerprint.fingerprint(channel, Fs=Fs)
    #         print(list(hashes))

    # # default sample rate of librosa is 22050
    # for file in glob.glob("wav/Yesterday/*.wav"):
    #     channels, Fs, file_hash = decoder.read(file, 10)
    #     print(Fs)
    #     y, sr = librosa.load(file)
    #     print(sr)

    # Genre
    # for file in glob.glob("Genres_original/pop/*.wav"):
    #     file_index = int(os.path.basename(file).split(".")[1])
    #     if file_index < 10:
    #         djv.fingerprint_file(file)

    # for file in glob.glob("Genres/*/*.wav"):
    #     pitch_shift(file)
    #     timbre_change(file)

    # for file in glob.glob("Genres_timbre/*/*.wav"):
    #     filter(file)

    # filter("blues.00000.wav")
    # song = djv.recognize(FileRecognizer, "blues.00000.wav")
    # print(song)

    arrs = {}
    for file in glob.glob("Genres/rock/*.wav"):
        song = djv.recognize(FileRecognizer, file)
        filename = os.path.basename(file).rsplit(".", 1)[0]
        songname = filename.split("_")[0]
        if song is not None:
            print("Actual:" + filename
                  + "\tPredicted:" + song['song_name']
                  + "\tConfidence:" + str(song['confidence'])
                  + "\tCorrectness:" + str(song['song_name'] == songname))
        else:
            print("Actual: " + filename + "\t\t" + "Predicted: " + song + "\tFalse")
        # print(song)

        file_index = int(os.path.basename(file).split(".")[1].split("_")[0])
        if file_index not in arrs:
            arrs[file_index] = [song['confidence']]
        else:
            if song['song_name'] == songname:
                arrs[file_index].append(song['confidence'])
            else:
                arrs[file_index].append(0)
    print(arrs)

    avg_orig = []
    avg = []
    for arr in arrs:
        a = arrs[arr]
        avg_orig.append(a[0])
        avg.append(a[1])
        avg.append(a[2])
        avg.append(a[3])

    mean_orig = np.mean(avg_orig)
    mean = np.mean(avg)
    print(mean_orig)
    print(mean)