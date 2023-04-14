import librosa
import soundfile as sf
from scipy import signal


def bandpass_filter(data, lowcut, highcut, fs, N=5):
    low = 2 * lowcut / fs
    high = 2 * highcut / fs
    b, a = signal.butter(N, [low, high], btype='bandpass')
    filtered = signal.filtfilt(b, a, data)
    return filtered


def filter(filepath, gain1=1, gain2=1, gain3=1, gain4=1, gain5=1, gain6=1, gain7=1, gain8=1, gain9=1):
    y, sr = librosa.load(filepath, sr=None)

    band1 = bandpass_filter(y, 22, 44, sr, 3) * gain1
    band2 = bandpass_filter(y, 44, 88, sr, 3) * gain2
    band3 = bandpass_filter(y, 88, 177, sr, 3) * gain3
    band4 = bandpass_filter(y, 177, 355, sr, 3) * gain4
    band5 = bandpass_filter(y, 355, 710, sr, 3) * gain5
    band6 = bandpass_filter(y, 710, 1420, sr, 3) * gain6
    band7 = bandpass_filter(y, 1420, 2840, sr, 3) * gain7
    band8 = bandpass_filter(y, 2840, 5680, sr, 3) * gain8
    band9 = bandpass_filter(y, 5680, 7999, sr, 3) * gain9

    filtered = band1 + band2 + band3 + band4 + band5 + band6 + band7 + band8 + band9
    filepath = filepath.rsplit(".", 1)[0]

    if gain1 == 0:
        sf.write(filepath + "_timbre1.wav", filtered, sr)
        print(filepath + "_timbre1.wav" + " created")
    if gain4 == 0:
        sf.write(filepath + "_timbre2.wav", filtered, sr)
        print(filepath + "_timbre2.wav" + " created")
    if gain7 == 0:
        sf.write(filepath + "_timbre3.wav", filtered, sr)
        print(filepath + "_timbre3.wav" + " created")


# def filter(filepath):
#     y, sr = librosa.load(filepath)
#     b, a = signal.butter(8, [0.1, 0.3], 'bandpass')  # 配置滤波器 8 表示滤波器的阶数
#     filtered = signal.filtfilt(b, a, y)
#     filepath = filepath.rsplit(".", 1)[0]
#     sf.write(filepath + "_timbre_1.wav", filtered, sr)
#
#     b, a = signal.butter(8, [0.5, 0.7], 'bandpass')
#     filtered1 = signal.filtfilt(b, a, y)
#     sf.write(filepath + "_timbre_2.wav", filtered1, sr)
#
#     filtered2 = filtered + filtered1
#     sf.write(filepath + "_timbre_3.wav", filtered2, sr)


def timbre_change(filepath):
    y, sr = librosa.load(filepath)

    # stft 短时傅立叶变换
    a = librosa.stft(y)
    length = len(a)
    # magnitude
    # a = abs(a)

    # 改变或去除某些值，可以改变声音
    r_a = a[0:length - 10]

    # istft 逆短时傅立叶变换，变回去
    b = librosa.istft(r_a)

    # # resample
    # b = librosa.resample(b, sr, 16000)

    # librosa.output.write_wav("stft.wav", b, sr)
    filepath = filepath.rsplit(".", 1)[0]
    sf.write(filepath + "_timbre.wav", b, sr)
    print(filepath + "_timbre.wav" + " created")

    # 以下是显示频谱图
    # fig = plt.figure()
    # s1 = fig.add_subplot(3, 1, 1)
    # s2 = fig.add_subplot(3, 1, 2)
    # s3 = fig.add_subplot(3, 1, 3)
    #
    # s1.plot(y)
    # s2.plot(a)
    # s3.plot(b)
    #
    # plt.show()
