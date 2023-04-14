import librosa
import soundfile as sf


def pitch_shift(filepath):
    y, sr = librosa.load(filepath, sr=None)
    filepath = filepath.rsplit(".", 1)[0]

    # 通过移动音调变声 ，14是上移14个半步， 如果是 -14 下移14个半步
    for i in range(3):
        b = librosa.effects.pitch_shift(y, sr, n_steps=i + 1)

        # resample
        # b = librosa.resample(b, sr, 16000)

        sf.write(filepath + "_{}.wav".format(i + 1), b, sr)
        print(filepath + "_{}.wav".format(i + 1) + " created")
