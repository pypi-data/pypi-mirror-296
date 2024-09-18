# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
"""
Test the likelihood classes
"""
import unittest
import logging
import numpy as np
import lisagwresponse
from matplotlib import pyplot as plt
from backgrounds import StochasticPointSourceResponse, utils
from lisagwresponse import StochasticPointSource
from backgrounds import signal, SignalPSD
from backgrounds import SplineNoiseModel
from backgrounds.tdi import compute_tdi_tf, aet_mat


logging.basicConfig()
# logging.getLogger('lisagwresponse').setLevel(logging.INFO)


class TestLikelihoods(unittest.TestCase):

    def test_signal_psd(self, plot=False):

        orbits = 'tests/orbits/keplerian-orbits.h5'
        pixel_generator = lisagwresponse.psd.ifft_generator(signal.sgwb_psd)
        gw_lambda = 0
        gw_beta = 0

        dt = 50.0
        size = int(14 * 24 * 3600 / dt)
        t0 = 10.0

        src_class = StochasticPointSource(
            pixel_generator,
            gw_lambda=gw_lambda,
            gw_beta=gw_beta,
            orbits=orbits,
            dt=dt, size=size, t0=t0)

        # Instantiate analytical response
        resp_class = StochasticPointSourceResponse.from_gw(src_class)

        # Choosing a subset of frequencies
        f1 = 1 / (size * dt)
        f2 = 1 / (2 * dt)
        nf = 500
        freq = f1 * (f2/f1) ** (np.arange(0, nf) / (nf-1))

        # Compute the response kernel for TDI AET on a subset of frequencies
        g_mat_aet = resp_class.compute_tdi_kernel(
            freq, size * dt / 2, tdi_var='aet')

        signal_psd = SignalPSD(freq, g_mat_aet, signal.sgwb_psd,
                               gw_log_psd=None, sgwb_kwargs={})

        theta = np.array([np.log(1.0), 0.5])

        psd_1 = signal_psd.compute_psds(theta)[:, 0]
        psd_2 = g_mat_aet[:, 0, 0] * signal.sgwb_psd(freq)

        if plot:
            plt.figure(0)
            plt.loglog(freq, np.sqrt(psd_1), label='Signal class')
            plt.loglog(freq, np.sqrt(psd_2), label='Direct computation',
            linestyle='dashed')
            plt.show()

        np.testing.assert_array_almost_equal(psd_1, psd_2)

    def test_noise_psd(self):

        orbits = 'tests/orbits/keplerian-orbits.h5'

        # Sampling and size
        dt = 50.0
        size = int(14 * 24 * 3600 / dt)
        t0 = 10.0

        # Fourier frequencies
        freqs = np.fft.fftfreq(size) / dt

        # Restrict analysis
        inds = np.where(freqs > 0)[0]

        # Instantiate SGWB class
        src_class = StochasticPointSource(
            lisagwresponse.psd.ifft_generator(signal.sgwb_psd),
            gw_lambda=0.0,
            gw_beta=0.0,
            orbits=orbits,
            dt=dt, size=size, t0=t0)

        # TDI XYZ transfer function
        transform_xyz = compute_tdi_tf(freqs[inds], src_class.ltt, size * dt / 2,
                                       gen='2.0')
        # TDI AET
        transform_aet = utils.multiple_dot(
            aet_mat[np.newaxis, :, :], transform_xyz)
        # Choosing spline degree
        degree = 3

        # Choosing frequencies knots
        n_knots = 6
        f0 = 1e-4
        f1 = 9e-3
        f_knots = f0 * (f1/f0)**(np.arange(0, n_knots)/(n_knots-1))

        # Instantiate noise model
        noise_model = SplineNoiseModel(freqs[inds], f_knots, degree, transform_aet,
                                       hypertriangle=True)


if __name__ == '__main__':
    # unittest.main()
    test = TestLikelihoods()
    test.test_signal_psd(plot=True)
