# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
"""
Test the StochasticPointSourceResponse and StochasticBackgroundResponse classes
"""
import logging
import pytest
import numpy as np
import healpy as hp
import lisagwresponse
from scipy import signal
from matplotlib import pyplot as plt
from backgrounds import StochasticPointSourceResponse, StochasticBackgroundResponse
from backgrounds import sgwb_psd
from lisagwresponse import StochasticPointSource, StochasticBackground

logging.basicConfig()
# logging.getLogger('lisagwresponse').setLevel(logging.INFO)


def white_generator(fs, size,  psd=1.0):
    stddev = np.sqrt(psd * fs / 2)
    return np.random.normal(scale=stddev, size=size)


# @pytest.mark.parametrize('plot', [False])
class TestLikelihoods:
    def test_point_source_response(self, plot1):

        test_path = os.path.dirname(os.path.abspath(__file__))
        orbits = test_path[:-5] + 'data/keplerian-orbits.h5'
        pixel_generator = lisagwresponse.psd.ifft_generator(sgwb_psd)

        gw_lambda = 0
        gw_beta = 0
        dt = 10.0
        size = int(14 * 24 * 3600 / dt)
        t0 = 10.0

        src_class = StochasticPointSource(
            pixel_generator,
            gw_lambda=gw_lambda,
            gw_beta=gw_beta,
            orbits=orbits,
            dt=dt, size=size, t0=t0)

        # Generate the response
        t = t0 + np.arange(size) * dt
        response = src_class.compute_gw_response(t, src_class.LINKS)
        # Compute the analytical response
        resp_class = StochasticPointSourceResponse.from_gw(src_class)
        # Choosing a subset of frequencies
        f1 = 1 / (size * dt)
        f2 = 1 / (2 * dt)
        nf = 500
        f_subset = f1 * (f2/f1) ** (np.arange(0, nf) / (nf-1))
        # Compute single-link response at middle time
        t0_resp = size * dt / 2.0
        g_plus_mat, g_cross_mat = resp_class.compute_correlations(
            src_class.LINKS, f_subset, np.array([t0_resp]))
        resp_mat = (g_plus_mat + g_cross_mat) * sgwb_psd(f_subset)[:, np.newaxis, np.newaxis]

        # Compare periodograms and model
        response_pers = [signal.welch(
            resp, fs=1/dt, window='blackman', nperseg=int(48*3600/dt), return_onesided=True)
            for resp in response]

        if plot1:
            plt.figure(0)
            plt.loglog(response_pers[0][0], np.sqrt(
                response_pers[0][1]), label='Welch periodogram')
            plt.loglog(f_subset, np.sqrt(
                np.abs(resp_mat[:, 0, 0])), label='Analytic response')
            plt.show()

        assert resp_class.x is not None

    def test_background_response(self, plot2):

        orbits = '../data/keplerian-orbits.h5'
        npix = hp.nside2npix(4)
        m = np.ones(npix)

        dt = 50.0
        size = int(14 * 24 * 3600 / dt)
        t0 = 10.0

        # Instantiate background class
        src_class = StochasticBackground(
            skymap=m,
            generator=white_generator,
            orbits=orbits,
            dt=dt, size=size, t0=t0, optim=True)

        # Generate the background
        t = t0 + np.arange(size) * dt
        response = src_class.compute_gw_response(t, src_class.LINKS)

        # Instantiate the response function
        resp_class = StochasticBackgroundResponse.from_gw(src_class)

        # Choosing a subset of frequencies
        f1 = 1 / (size * dt)
        f2 = 1 / (2 * dt)
        nf = 500
        f_subset = f1 * (f2/f1) ** (np.arange(0, nf) / (nf-1))
        # Compute single-link response at middle time
        t0_resp = size * dt / 2.0
        g_plus_mat, g_cross_mat = resp_class.compute_correlations(
            src_class.LINKS, f_subset, np.array([t0_resp]))
        resp_mat = g_plus_mat + g_cross_mat

        # Compare periodograms and model
        response_pers = [signal.welch(
            resp, fs=1/dt, window='blackman', nperseg=int(48*3600/dt), return_onesided=True)
            for resp in response]

        if plot2:
            plt.figure(0)
            plt.loglog(response_pers[0][0], np.sqrt(
                response_pers[0][1]), label='Welch periodogram')
            plt.loglog(f_subset, np.sqrt(
                np.abs(resp_mat[:, 0, 0])), label='Analytic response')
            plt.show()

        assert resp_class.x is not None
