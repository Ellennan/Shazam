import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import (generate_binary_structure, iterate_structure, binary_erosion)
import hashlib
from operator import itemgetter
import librosa

IDX_FREQ_I = 0
IDX_TIME_J = 1

######################################################################
# Sampling rate, related to the Nyquist conditions, which affects
# the range frequencies we can detect.
DEFAULT_FS = 44100

######################################################################
# Size of the FFT window, affects frequency granularity
DEFAULT_WINDOW_SIZE = 4096

######################################################################
# Ratio by which each sequential window overlaps the last and the
# next window. Higher overlap will allow a higher granularity of offset
# matching, but potentially more fingerprints.
DEFAULT_OVERLAP_RATIO = 0.5

######################################################################
# Degree to which a fingerprint can be paired with its neighbors --
# higher will cause more fingerprints, but potentially better accuracy.
DEFAULT_FAN_VALUE = 15

######################################################################
# Minimum amplitude in spectrogram in order to be considered a peak.
# This can be raised to reduce number of fingerprints, but can negatively
# affect accuracy.
DEFAULT_AMP_MIN = 10

######################################################################
# Number of cells around an amplitude peak in the spectrogram in order
# for Dejavu to consider it a spectral peak. Higher values mean less
# fingerprints and faster matching, but can potentially affect accuracy.
PEAK_NEIGHBORHOOD_SIZE = 20

######################################################################
# Thresholds on how close or far fingerprints can be in time in order
# to be paired as a fingerprint. If your max is too low, higher values of
# DEFAULT_FAN_VALUE may not perform as expected.
MIN_HASH_TIME_DELTA = 0
MAX_HASH_TIME_DELTA = 200

######################################################################
# If True, will sort peaks temporally for fingerprinting;
# not sorting will cut down number of fingerprints, but potentially
# affect performance.
PEAK_SORT = True

######################################################################
# Number of bits to throw away from the front of the SHA1 hash in the
# fingerprint calculation. The more you throw away, the less storage, but
# potentially higher collisions and misclassifications when identifying songs.
FINGERPRINT_REDUCTION = 20


def fingerprint(channel_samples, Fs=DEFAULT_FS,
                wsize=DEFAULT_WINDOW_SIZE,
                wratio=DEFAULT_OVERLAP_RATIO,
                fan_value=DEFAULT_FAN_VALUE,
                amp_min=DEFAULT_AMP_MIN):
    """
    FFT the channel, log transform output, find local maxima, then return locally sensitive hashes.
    """
    # FFT the signal and extract frequency components
    spectrum, freqs, t = mlab.specgram(channel_samples,
                                       NFFT=wsize,
                                       Fs=Fs,
                                       window=mlab.window_hanning,
                                       noverlap=int(wsize * wratio)
                                       )

    # channel_samples = channel_samples.astype(float)
    # constant-q transform
    # C = np.abs(librosa.cqt(channel_samples, Fs))
    # C = librosa.feature.melspectrogram(y=channel_samples, sr=Fs)

    # # plot spectrogram(myself)
    # plt.specgram(channel_samples,
    #              NFFT=wsize,
    #              Fs=Fs,
    #              window=mlab.window_hanning,
    #              noverlap=int(wsize * wratio),
    #              cmap="jet"
    #              )
    # plt.colorbar()
    # plt.xlabel('Time')
    # plt.ylabel('Frequency')
    # plt.title("Spectrogram")
    # plt.savefig('specgram.png')
    # plt.show()

    # print("freqs shape: {}".format(freqs.shape))
    # print("t: {}".format(t))
    # print("Spectrum shape: {}".format(spectrum.shape))

    # replace all 0 with 1 to avoid log(0) appear since the intensity is 0 and log(1) = 0
    spectrum[spectrum == 0] = 1
    spectrum = 10 * np.log10(spectrum)
    # apply log transform since specgram() returns linear array
    # arr2D = 10 * np.log10(arr2D + 1e-5)
    # arr2D[arr2D == -np.inf] = 0  # replace infs with zeros

    # find local maxima
    local_maxima = get_2D_peaks(spectrum, freqs, t, plot=False, amp_min=amp_min)
    # print(local_maxima)

    # return hashes
    return generate_hashes(local_maxima, fan_value=fan_value)


def get_2D_peaks(arr2D, freqs, t, plot=False, amp_min=DEFAULT_AMP_MIN):
    # http://docs.scipy.org/doc/scipy/reference/generated/scipy.ndimage.morphology.iterate_structure.html#scipy.ndimage.morphology.iterate_structure
    struct = generate_binary_structure(2, 1)
    neighborhood = iterate_structure(struct, PEAK_NEIGHBORHOOD_SIZE)

    # find local maxima using our filter shape
    local_max = maximum_filter(arr2D, footprint=neighborhood) == arr2D
    background = (arr2D == 0)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # Boolean mask of arr2D with True at peaks
    detected_peaks = local_max ^ eroded_background

    # extract peaks
    amps = arr2D[detected_peaks]
    j, i = np.where(detected_peaks)

    # filter peaks
    amps = amps.flatten()
    peaks = zip(i, j, amps)
    peaks_filtered = [x for x in peaks if x[2] > amp_min]  # freq, time, amp

    # get indices for frequency and time
    frequency_idx = [x[1] for x in peaks_filtered]
    time_idx = [x[0] for x in peaks_filtered]

    frequency = [int(freqs[i]) for i in frequency_idx]
    time = [round(t[i], 3) for i in time_idx]

    if plot:
        # plot constellation map(myself)
        fig, ax = plt.subplots()
        ax.scatter(time, frequency)
        ax.set_xlabel('Time')
        ax.set_ylabel('Frequency')
        ax.set_title("Constellation Map")
        plt.xticks(np.arange(0, 11))
        plt.yticks(np.arange(0, 12000, step=2000))
        # plt.savefig('constellation.png')
        plt.show()

    return list(zip(frequency, time))


def generate_hashes(peaks, fan_value=DEFAULT_FAN_VALUE):
    """
    Hash list structure:
       sha1_hash[0:20]    time_offset
    [(e05b341a9b77a51fd26, 32), ... ]
    """
    if PEAK_SORT:
        sorted(peaks, key=itemgetter(1))

    for i in range(len(peaks)):
        for j in range(1, fan_value):
            if (i + j) < len(peaks):

                freq1 = peaks[i][IDX_FREQ_I]
                freq2 = peaks[i + j][IDX_FREQ_I]
                f_delta = freq2 - freq1
                t1 = peaks[i][IDX_TIME_J]
                t2 = peaks[i + j][IDX_TIME_J]
                t_delta = t2 - t1

                if MIN_HASH_TIME_DELTA <= t_delta <= MAX_HASH_TIME_DELTA:
                    data = str(freq1) + "|" + str(freq2) + "|" + str(t_delta)
                    # data = str(f_delta) + "|" + str(t_delta)
                    h = hashlib.sha1(data.encode("utf-8"))
                    # print(h.hexdigest())
                    # h = hashlib.sha1("%s|%s|%s".encode("utf-8") % (str(freq1), str(freq2), str(t_delta)))
                    yield h.hexdigest()[0:FINGERPRINT_REDUCTION], t1
