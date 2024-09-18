# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
# This code provides routines for PSD estimation using a peace-continuous model
# that assumes that the logarithm of the PSD is linear per peaces.
import numpy as np
from scipy import optimize
from scipy import signal as sig
from scipy.signal.windows import blackmanharris, nuttall
# FTT modules
try:
    import pyfftw
    from pyfftw.interfaces.numpy_fft import fft, ifft
except ImportError:
    from numpy.fft import fft, ifft
from . import utils

try:
    from pywavelet.transforms import from_time_to_wavelet
    from pywavelet.transforms.types import TimeSeries
except ImportError:
    pass


def periodogram(x, fs, wd_func=blackmanharris, wisdom=None):
    """Compute the periodogram of a time series using the
    Blackman window

    Parameters
    ----------
    x : ndarray
        intput time series
    fs : float
        sampling frequency
    wd_func : callable
        tapering window function in the time domain

    Returns
    -------
    ndarray
        periodogram at Fourier frequencies
    """

    # Getting some FFT plan wisdom to speed up
    if wisdom is not None:
        pyfftw.import_wisdom(wisdom)

    wd = wd_func(x.shape[0])
    k2 = np.sum(wd**2)
    if x.ndim == 1:
        per = np.abs(fft(x * wd))**2 * 2 / (k2*fs)
    elif x.ndim == 2:
        per = np.abs(fft(x * wd[:, np.newaxis], axis=0))**2 * 2 / (k2*fs)

    return per


def spectrogram(x, fs, nf, nt, mult=4):
    """Compute the spectrogram of a time series using the 
    WDM wavelet transform

    Parameters
    ----------
    x : ndarray
        intput time series
    fs : float
        sampling frequency

    Returns
    -------
    ndarray
        spectrogram at wavelet time and frequency bins
        size nf x nt
    """

    x_time_obj = TimeSeries(x, time=np.arange(x.size) / fs)
    x_wavelet = from_time_to_wavelet(x_time_obj, Nf=nf, Nt=nt, mult=mult)

    return np.abs(x_wavelet)**2 * 2.0 / fs # To be consistent with a PSD


def cross_periodogram(x, y, fs, wd_func=blackmanharris, wisdom=None):
    """Compute the cross-periodogram of two time series using the
    Blackman window

    Parameters
    ----------
    x : ndarray
        first intput time series
    y : ndarray
        second intput time series
    fs : float
        sampling frequency
    wd_func : callable
        tapering window function in the time domain

    Returns
    -------
    ndarray
        periodogram at Fourier frequencies
    """

    # Getting some FFT plan wisdom to speed up
    if wisdom is not None:
        pyfftw.import_wisdom(wisdom)

    wd = wd_func(x.shape[0])
    k2 = np.sum(wd**2)
    x_wfft = fft(x * wd)
    y_wfft = fft(y * wd)
    return x_wfft * np.conj(y_wfft) * 2 / (k2*fs)


def cross_spectrogram(x, y, fs, nf, nt, mult=4):
    """Compute the cross spectrogram of two time series using the 
    WDM wavelet transform

    Parameters
    ----------
    x : ndarray
        first intput time series
    y : ndarray
        second intput time series
    fs : float
        sampling frequency

    Returns
    -------
    ndarray
        spectrogram at wavelet time and frequency bins
        size nf x nt
    """
    
    time_vector = np.arange(x.size) / fs
    x_time_obj = TimeSeries(x, time=time_vector)
    x_wavelet = from_time_to_wavelet(x_time_obj, Nf=nf, Nt=nt, mult=mult)
    y_time_obj = TimeSeries(y, time=time_vector)
    y_wavelet = from_time_to_wavelet(y_time_obj, Nf=nf, Nt=nt, mult=mult)
    
    return x_wavelet * y_wavelet * 2 / fs


def periodogram_matrix(x_list, fs, wd_func=blackmanharris, wisdom=None, transform=None):
    """
    Computes the matrix of periodograms and cross periodograms of the 
    multivariate time series x_list.
    

    Parameters
    ----------
    x_list : list of ndarrays
        list of intput time series. They should all have the same size N.
    fs : float
        sampling frequency
    wd_func : callable
        tapering window function in the time domain
    transform : ndarray or None
        transfer function to apply in the frequency domain

    Returns
    -------
    ndarray
        periodogram matrix of size N x p x p where p is the length of x_list.
    
    """

    # Getting some FFT plan wisdom to speed up
    if wisdom is not None:
        pyfftw.import_wisdom(wisdom)

    # n_c = len(x_list)
    # mat = np.zeros((x_list[0].shape[0], n_c, n_c), dtype=complex)

    # for i in range(n_c):
    #     mat[:, i, i] = periodogram(x_list[i], fs, 
    #                                wd_func=wd_func,
    #                                wisdom=wisdom, transform=transform).real

    #     for j in range(i+1, n_c):
    #         mat[:, i, j] = cross_periodogram(x_list[i], x_list[j], fs,
    #                                          wd_func=wd_func,
    #                                          wisdom=wisdom, transform=transform)
    #         mat[:, j, i] = np.conj(mat[:, i, j])

    # Transform data to array
    x_arr = np.asarray(x_list, dtype=complex).T
    n_data = x_arr.shape[0]
    # Compute the window
    wd = wd_func(n_data)
    # Norm related to windowing
    k2 = np.sum(wd**2)
    # Fourier transform the whole vector (size n_data x p)
    x_tf = fft(wd[:, np.newaxis] * x_arr, axis=0) * np.sqrt(2 / (k2*fs))
    # Apply transfer function if necessary
    if transform is not None:
        x_tf = utils.multiple_dot_vect(transform, x_tf)
    # Compute the periodogram matrix
    mat = utils.multiple_dot(x_tf[:, :, np.newaxis], np.conj(x_tf[:, np.newaxis, :]))

    return mat


def stft_matrix(x_list, fs, nperseg, **kwargs):
    """
    Computes the matrix of short-time Fourier transform periodograms 
    and cross periodograms of the multivariate time series x_list.
    

    Parameters
    ----------
    x_list : list of ndarrays
        list of intput time series. They should all have the same size N.
    fs : float
        sampling frequency
    nperseg : int
        size of semgents
    wd_func : callable
        tapering window function in the time domain

    Returns
    -------
    ndarray
        periodogram matrix of size N x p x p where p is the length of x_list.
    
    """

    # Initialization
    f_bins, t_bins, x0_stft = sig.stft(x_list[0], fs=fs, nperseg=nperseg, **kwargs)
    nc = len(x_list)
    nt = len(t_bins)
    nf = len(f_bins)
    mat = np.zeros((nf, nt, nc, nc), dtype=complex)
    mat[..., 0, 0] = x0_stft

    for i in range(nc):
        if i != 0:
            f_bins, t_bins, xi_stft = sig.stft(x_list[i], fs=fs, nperseg=nperseg, **kwargs)
        else:
            xi_stft = x0_stft
        mat[..., i, i] = np.abs(xi_stft)**2

        for j in range(i+1, nc):
            _, _, xj_stft = sig.stft(x_list[i], fs=fs, nperseg=nperseg, **kwargs)
            mat[..., i, j] = xi_stft * xj_stft
            mat[..., j, i] = np.conj(mat[..., i, j])

    return f_bins, t_bins, 2*mat


def spectrogram_matrix(x_list, fs, nf, nt, mult=4):
    """
    Computes the matrix of wavelet spectrograms and cross spectrograms of the 
    multivariate time series x_list.
    

    Parameters
    ----------
    x_list : list of ndarrays
        list of intput time series. They should all have the same size N.
    fs : float
        sampling frequency
    wd_func : callable
        tapering window function in the time domain

    Returns
    -------
    ndarray
        periodogram matrix of size N x p x p where p is the length of x_list.
    
    """

    n_c = len(x_list)
    mat = np.zeros((nf, nt, n_c, n_c), dtype=float)

    for i in range(n_c):
        mat[..., i, i] = spectrogram(x_list[i], fs, nf, nt, mult=mult)

        for j in range(i+1, n_c):
            mat[..., i, j] = cross_spectrogram(x_list[i], x_list[j], fs,
                                             nf, nt, mult=mult)
            mat[..., j, i] = mat[..., i, j]

    return mat


def welch(x, fs, nperseg, wd_func=blackmanharris):
    """Welch periodogram with non-overlapping segments

    Parameters
    ----------
    x : ndarray
        intput time series
    fs : float
        sampling frequency
    nperseg : int
        segment size
    wd_func : callable
        tapering window function in the time domain

    Returns
    -------
    ndarray
        Welch periodogram
    """

    k_seg = x.shape[0] // nperseg
    per = sum([periodogram(x[j*nperseg:(j+1)*nperseg], fs, wd_func=wd_func)
               for j in range(k_seg)]) / k_seg

    return per


def welch_csd(x, y, fs, nperseg, wd_func=blackmanharris):
    """Welch periodogram with non-overlapping segments

    Parameters
    ----------
    x : ndarray
        first intput time series
    y : ndarray
        second intput time series
    fs : float
        sampling frequency
    nperseg : int
        segment size
    wd_func : callable
        tapering window function in the time domain

    Returns
    -------
    ndarray
        Welch periodogram
    """

    k_seg = x.shape[0] // nperseg
    per = sum([cross_periodogram(x[j*nperseg:(j+1)*nperseg], y[j*nperseg:(j+1)*nperseg], fs,
                                wd_func=wd_func)
               for j in range(k_seg)]) / k_seg

    return per


def welch_matrix(x_list, fs, nperseg, wd_func=blackmanharris,
                 output_freqs=False):
    """Computes all Welch cross-periodograms for a list 
    of synchronous time series.

    Parameters
    ----------
    x_list : list or ndarray
        list of n_c intput time series of size n
    fs : float
        sampling frequency
    nperseg : int, or array_like
        segment size. If freq_segments is provided, must
        be a vector of size len(freq_segments) - 1
    wd_func : callable
        tapering window function in the time domain
    output_freqs : bool
        If True, outputs frequency abscissa
        

    Returns
    -------
    ndarray
        Welch periodogram matrix, size nperseg x n_c x n_c
    """ 

    k_seg = x_list[0].shape[0] // nperseg
    per = sum([periodogram_matrix([x[j*nperseg:(j+1)*nperseg] for x in x_list], fs,
                                 wd_func=wd_func)
               for j in range(k_seg)]) / k_seg

    if output_freqs:
        f_per = np.fft.fftfreq(nperseg) * fs

        return f_per, per
    else:
        return per


def welch_matrix_adaptive(x_list, fs, nperseg, freq_segments, wd_func=blackmanharris,
                          output_freqs=False):
    """Computes all Welch cross-periodograms for a list 
    of synchronous time series, with adaptative averaging depending 
    on frequency segments.

    Parameters
    ----------
    x_list : list or ndarray
        list of n_c intput time series of size n
    fs : float
        sampling frequency
    nperseg : int, or array_like
        time segment size. Must be a vector of size len(freq_segments) - 1
    freq_segments : ndarray
        Frequency segments bounds. To have frequency-dependent averaging. 
        Periodograms ordinates between frequencies 
        freq_segments[j] and freq_segments[j+1] are computed
        by averaging n/nperseg[j] segments of size nperseg[j]
    wd_func : callable
        tapering window function in the time domain
    output_freqs : bool
        if True, outputs the Welch frequency vector

    Returns
    -------
    f_per : ndarray
        Frequency abscissa, size J
    per : ndarray
        Welch periodogram matrix, size J x n_c x n_c
    k_seg_vect :
        Number of time segments averaged to compute P(f)
        as a function of f.

    """

    # Number of frequency segments
    n_seg = len(freq_segments)-1
    # Number of time segments
    f_per_full = [np.fft.fftfreq(nperseg[q]) * fs for q in range(n_seg)]
    ii = [np.where((f_per_full[q]>=freq_segments[q]) & (f_per_full[q]<freq_segments[q+1]))[0]
          for q in range(n_seg)]
    # Welch matrix for each time segment sizes
    per = np.vstack([welch_matrix(x_list, fs, nperseg[q], wd_func=wd_func)[ii[q]]
                       for q in range(n_seg)])
    # Stacked frequencies
    f_per = np.hstack([f_per_full[q][ii[q]] for q in range(n_seg)])
    # Vector of segment sizes as a function of frequencies
    k_seg_vect = np.hstack([x_list[0].shape[0] // nperseg[q] * np.ones(len(ii[q]))
                            for q in range(n_seg)])

    if output_freqs:
        return f_per, per, k_seg_vect
    else:
        return per, k_seg_vect


def taper_window(nu, nu0, m):

    return 1 / (1 + (nu / nu0)**(2*m))


def rect_window(nu, k0):
    """
    Fourier transform of the rectangular window
    centered in 0 and of length k0

    Parameters
    ----------
    nu : ndarray
        normalized frequency vector
    k0 : int
        width of the window, in number of samples

    Returns
    -------
    ndarray
        window in the frequency domain
    """

    out = np.zeros_like(nu)
    out[nu == 0] = 1.0
    out[nu != 0] = np.sin((2*k0+1)*np.pi*nu[nu != 0]) / \
        (np.sin(np.pi * nu[nu != 0])) / (2*k0+1)

    return out


def frequency_grid(df_min, df_max, f_min, f_max):
    """
    Produces a grid of frequencies linearly spaced, such that
    the number of Fourier bins between 2 consecutive grid frequencies 
    increases linearly as a function of frequency.

    Parameters
    ----------
    df_min : float
        minimum frequency separation between two bins
    df_max: float
        maximum frequency separation between two bins
    f_min : float
        smallest frequency of the grid
    f_max : float
        largest frequency of the grid

    Returns
    -------
    frequencies : ndarray
        frequency grid vector defining the segmentation of the Fourier space
    """

    # Frequency bandwidth
    df_tot = f_max - f_min
    # Constraint on the number of grid points
    n_grid = round(2 * df_tot / (df_min + df_max))
    # Logarithmic grid for the frequency spacings
    df_grid = df_min + np.arange(0, n_grid)/(n_grid-1) * (df_max - df_min)
    # Frequency grid
    f_grid = f_min + np.cumsum(df_grid)

    return f_grid


def smooth(y, fs, f_seg, weights_func=None):
    """
    Smooth the frequency-domain data.

    Parameters
    ----------
    y : ndarray
        periodogram array, size n_freq x n_channels
    fs : float
        sampling frequency OR frequency vector corresponding to y
    f_seg : float or ndarray
        segment frequencies

    Returns
    -------
    freqs_h : ndarray
        frequencies where the smoothed log-periodogram is computed
    p_h : ndarray
        smoothed periodogram at frequencies freqs_h
    f_seg : ndarray
        Frequencies of segment edges

    """
    x_shape = y.shape
    if isinstance(fs, float):
        freqs = np.fft.fftfreq(x_shape[0]) * fs
        # Observation duration
        # t_obs = x_shape[0] / fs
    else:
        # Assume that fs is already the vector of frequencies
        freqs = np.copy(fs)

    if isinstance(f_seg, float):
        # Smoothing bandwidth
        bandwidth = int(f_seg / (fs/x_shape[0]))
        # Segment frequencies
        f_seg_arr = freqs[freqs>=0][0::bandwidth]
    elif isinstance(f_seg, (np.ndarray, list)):
        f_seg_arr = np.asarray(f_seg)
    else:
        raise TypeError("f0 should be a float or array_like")
    # Number of segments
    n_seg = len(f_seg_arr)
    # Indices of the segment bounds
    i_seg = np.asarray([np.argmin(np.abs(freqs-fc)) for fc in f_seg_arr])
    # i_seg = np.round(f_seg_arr * t_obs).astype(int)
    # Sizes of all intervals
    segment_sizes = i_seg[1:] - i_seg[:-1]
    # Middle frequencies
    freqs_h = (f_seg_arr[:-1] + f_seg_arr[1:]) / 2.0
    # Weighting?
    if weights_func is None:
        weights_func = np.ones

    weights = [weights_func(ss) for ss in segment_sizes]
    normalisations = [np.sum(w) for w in weights]
    # If y is a spectrogram matrix
    if len(np.shape(y)) == 4:
        weights_vector = [w[:, np.newaxis, np.newaxis, np.newaxis]
                          for w in weights]
    # If y is a periodogram matrix
    elif len(np.shape(y)) == 3:
        weights_vector = [w[:, np.newaxis, np.newaxis]
                          for w in weights]
    # If y is a vector of periodograms
    elif len(np.shape(y)) == 2:
        weights_vector = [w[:, np.newaxis] for w in weights]
    # If y is a periodogram
    elif len(np.shape(y)) == 1:
        weights_vector = weights
    # Compute the averages over each segment
    p_h = np.array(
        [np.sum(y[i_seg[j]:i_seg[j+1]]*weights_vector[j], axis=0)/normalisations[j]
         for j in range(n_seg-1)], dtype=y.dtype)

    return freqs_h, p_h, segment_sizes


def smoothed_log_periodogram(x, fs, f0=None):
    """
    Compute a smoothed log-periodogram to provide a sufficient statistics for
    the data analysis

    Parameters
    ----------
    x : ndarray
        time series
    fs : float
        sampling frequency
    f0 : float or ndarray
        width of smoothing kernel or segment frequencies

    Returns
    -------
    freqs_h : ndarray
        frequencies where the smoothed log-periodogram is computed
    logp_h : ndarray
        smoothed log-periodogram at frequencies freqs_h
    var : float
        variance of smoothed log-periodogram variables (except zero and Nyquist)

    """

    # Shape of input
    x_shape = x.shape
    # Signal raw periodograms
    if len(x_shape) == 2:
        pers_signal_raw = np.array(
            [periodogram(x[:, j], fs) for j in range(x_shape[1])]).T
    else:
        pers_signal_raw = periodogram(x, fs)
    # Compute the zero-mean log-periodogram variable y
    gamma = 0.5772156649
    nyquist = int((x_shape[0]-1)/2)
    y = np.log(pers_signal_raw) + gamma
    y[0, :] = np.log(pers_signal_raw[0, :]) + (np.log(2) + gamma) / np.pi
    y[nyquist+1] = np.log(pers_signal_raw[nyquist+1]) + \
        (np.log(2) + gamma) / np.pi

    freqs_h, logp_h, segment_sizes = smooth(y, fs, f_seg=f0)

    # Compute the frequency-dependant variances
    var = np.pi**2/(6*segment_sizes)

    return freqs_h, logp_h, var


def choose_frequency_knots(n_knots, freq_min=1e-5, freq_max=1.0, base=10):
    """Provide an array of frequency knots that are spaced logarithmically 
    according to a given base.

    Parameters
    ----------
    n_knots : int
        requested number of knots
    freq_min : float, optional
        minimum frequency, by default 1e-5
    freq_max : float, optional
        maximum frequency, by default 1.0
    base : int, optional
        logarithmic base, by default 10

    Returns
    -------
    ndarray
        knot frequencies
    """
    # Choose the frequency knots
    ns = - np.log(freq_min) / np.log(base)
    n0 = - np.log(freq_max) / np.log(base)
    jvect = np.arange(0, n_knots)
    alpha_guess = 0.8
    def targetfunc(x): return n0 - (1 - x ** (n_knots)) / (1 - x) - ns
    result = optimize.fsolve(targetfunc, alpha_guess)
    alpha = result[0]
    n_knots = n0 - (1 - alpha ** jvect) / (1 - alpha)
    f_knots = base ** (-n_knots)
    f_knots = f_knots[(f_knots > freq_min) & (f_knots < freq_max)]

    return np.unique(np.sort(f_knots))


def periodogram_mean(func, fs, n_data, wd_func, 
                     n_freq=None, n_points=None, n_conv=None, normal=True):
    """
    Compute the expectation of any periodogram depending on the time series
    size and the window function.
    
    Parameters
    ----------
    func: callable
        function returning the PSD vs frequency. Can return a PSD matrix.
    fs : float
        sampling frequency
    n_data : int
        size of the time series
    wd_func : callable
        time-domain tappering window function. Should take the data size as 
        an argument.
    n_freq : int, optional
        Size of the output frequency grid, with frequencies k f / n_freq
    n_points : int, optional
        Number of points used in the disrete approximation of the integral
    n_conv : int, optional
        number of points for the zero-padding of the window FFT
    
    Returns
    -------
    Pm_mat : ndarray
        Theoretical expectation of the periodogram matrix 
        with shape n_freq x p x p
    
    """

    if n_freq is None:
        n_freq = n_data
    if n_conv is None:
        n_conv = 2 * n_data - 1

    # Calculation of the sample autocovariance of the mask
    mask = wd_func(n_data)
    fx = fft(mask, n_conv)

    if normal:
        K2 = np.sum(mask ** 2)
    else:
        K2 = n_data
    lambda_N = np.real(ifft(fx * np.conj(fx))) / K2

    if n_points is None:
        n_points = 2 * n_data

    k_points = np.arange(0, n_points)
    frequencies = fs * (k_points / float(n_points) - 0.5)
    i = np.where(frequencies == 0)
    frequencies[i] = fs / (10 * n_points)

    # Compute the whole PSD matrix
    Z = func(frequencies)
    Z_ifft = ifft(Z, axis=0)
    n = np.arange(0, n_data)

    if len(np.shape(Z)) == 2:
        n = n[:, np.newaxis]
        lambda_N = lambda_N[:, np.newaxis]
    elif len(np.shape(Z)) == 3:
        n = n[:, np.newaxis, np.newaxis]
        lambda_N = lambda_N[:, np.newaxis, np.newaxis]

    R = fs / float(n_points) * (Z[0] * 0.5 * (np.exp(1j * np.pi * n) \
                                                 - np.exp(-1j * np.pi * n)) + n_points * Z_ifft[0:n_data] * np.exp(
        -1j * np.pi * n))

    # 3. Calculation of the of the periodogram mean vector
    X = R[0:n_data] * lambda_N[0:n_data]
    Pm_mat = fft(X, n_freq, axis=0) + n_freq * ifft(X, n_freq, axis=0) - R[0] * lambda_N[0]

    return Pm_mat * 2 / fs


def welch_expectation_adaptive(psd_func, fs, n_data, nperseg, wd_func, freq_segments,
                               output_freqs=False):
    """Computes the expectation of the Welch matrix for a list, with adaptative averaging depending 
    on frequency segments.

    Parameters
    ----------
    psd_func : callable
        True PSD function of frequency
    fs : float
        Sampling frequency
    n_data : int
        size of the entire time series
    nperseg : int, or array_like
        time segment sizes. Must be a vector of size len(freq_segments) - 1
    freq_segments : ndarray
        Frequency segments bounds. To have frequency-dependent averaging. 
        Periodograms ordinates between frequencies 
        freq_segments[j] and freq_segments[j+1] are computed
        by averaging n/nperseg[j] segments of size nperseg[j]
    wd_func : callable, default is blackmanharris
        Time window function (of data size)
    output_freqs : bool
        if True, outputs the Welch frequency vector


    Returns
    -------
    f_per : ndarray
        Frequency abscissa, size J
    per : ndarray
        Expectation of the Welch periodogram matrix, size J x n_c x n_c
    k_seg_vect :
        Number of time segments averaged to compute P(f)
        as a function of f.

    """

    # Number of frequency segments
    n_seg = len(freq_segments)-1
    # Number of time segments
    k_seg = [n_data // nperseg[q] for q in range(n_seg)]
    f_per_full = [np.fft.fftfreq(nperseg[q]) * fs for q in range(n_seg)]
    ii = [np.where((f_per_full[q]>=freq_segments[q]) & (f_per_full[q]<freq_segments[q+1]))[0]
          for q in range(n_seg)]
    # Welch matrix for each time segment sizes
    per = np.vstack([periodogram_mean(psd_func, fs, nperseg[q], wd_func)[ii[q]] 
                     for q in range(n_seg)])
    # Stacked frequencies
    f_per = np.hstack([f_per_full[q][ii[q]] for q in range(n_seg)])
    # Vector of segment sizes as a function of frequencies
    k_seg_vect = np.hstack([k_seg[q] * np.ones(len(ii[q])) for q in range(n_seg)])

    if output_freqs:
        return f_per, per, k_seg_vect
    else:
        return per, k_seg_vect


def normalized_equivalent_noise_bandwidth(wd_func, nd=2**10):
    """
    Compute the normalized equivalent noise bandwidth associated to a 
    time window

    Parameters
    ----------
    wd_func : callable
        window function
    nd : int
        size of the time series if known. Used only if the window is different from
        rectangular, blackman, hanning and nuttal.

    Returns
    -------
    nenbw : int
        normalized equivalent noise bandwidth
    """

    if wd_func is np.ones:
        nenbw = 1.0
    elif wd_func is np.blackman:
        nenbw = 1.726757479056736 # 2.0044
    elif wd_func is blackmanharris:
        nenbw = 2.0044
    elif wd_func is np.hanning:
        nenbw = 1.5000
    elif wd_func is nuttall:
        nenbw = 1.9761
    else:
        wd = wd_func(nd)
        nenbw = nd * np.sum(wd**2) / np.sum(wd)**2

    return nenbw
