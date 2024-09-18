# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
"""
Test the tdi.TDITransfer function class
"""
import logging
import numpy as np
import lisagwresponse
from matplotlib import pyplot as plt
from backgrounds import tdi
from lisagwresponse import StochasticPointSource

logging.basicConfig()
# logging.getLogger('lisagwresponse').setLevel(logging.INFO)


def sgwb_psd(f, n=0.5, f0=1e-3, omega_gw=1e-14, fmin=1e-5, h0=3.24e-18):
    """
    SGWB PSD in Hz^{-1}
    """

    f_shift = f + fmin
    omega_gw_f = omega_gw * (f_shift / f0) ** n
    h = (3*h0**2) * omega_gw_f / (4*np.pi**2 * f_shift**3)

    return h


def test_tdi_transfer_function(plot=False):

    test_path = os.path.dirname(os.path.abspath(__file__))
    orbits = test_path[:-5] + 'data/keplerian-orbits.h5'
    pixel_generator = lisagwresponse.psd.ifft_generator(sgwb_psd)

    # GW source parameters
    gw_lambda = 0
    gw_beta = 0
    # Sampling time
    dt = 10.0
    # Time series size
    size = int(14 * 24 * 3600 / dt)
    # Initial time
    t0 = 10.0

    # Instantiate GW source class
    src_class = StochasticPointSource(
        pixel_generator,
        gw_lambda=gw_lambda, gw_beta=gw_beta,
        orbits=orbits,
        dt=dt, size=size, t0=t0)

    # Generate the response
    t = t0 + np.arange(size) * dt
    response = src_class.compute_gw_response(src_class.LINKS, t)
    # Instantiate TDI transfer function
    tdi_tf = tdi.TDITransferFunction.from_gw(src_class, gen='2.0')

    # Choosing a subset of frequencies
    f1 = 1 / (size * dt)
    f2 = 1 / (2 * dt)
    nf = 500
    frequencies = f1 * (f2/f1) ** (np.arange(0, nf) / (nf-1))

    # Compute the TDI transfer function at the initial time
    tdi_mat = tdi_tf.compute_tf(frequencies, t0)

    if plot:
        plt.figure(0)
        plt.loglog(frequencies, np.sqrt(
            np.abs(tdi_mat[:, 0, 0])), label='Analytic transfer function for TDI X')
        plt.show()


if __name__ == '__main__':

    test_tdi_transfer_function(plot=True)


