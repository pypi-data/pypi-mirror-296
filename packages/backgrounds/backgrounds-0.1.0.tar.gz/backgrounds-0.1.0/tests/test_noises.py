# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2023 <quentin.baghi@protonmail.com>
"""
Test the noise model classes
"""
import unittest
import os
import logging
import numpy as np
import healpy as hp
from matplotlib import pyplot as plt
from backgrounds import noise, tdi, StochasticBackgroundResponse
logging.basicConfig()


def prepare_input(dt=10.0, size=int(14 * 24 * 3600 / 10.0), t0=10.0):

    # Choosing a subset of frequencies
    f1 = 1 / (size * dt)
    f2 = 1 / (2 * dt)
    nf = 500
    f_subset = f1 * (f2/f1) ** (np.arange(0, nf) / (nf-1))
    
    # Time vector
    t_vect = np.arange(0, size) * dt
                  
    # Instantiate SGWB class
    test_path = os.path.dirname(os.path.abspath(__file__))
    orbits = test_path[:-5] + 'data/keplerian-orbits.h5'
    print(orbits)
    npix = hp.nside2npix(8)
    m = np.ones(npix) / np.sqrt(npix)
    sgwb_cls = StochasticBackgroundResponse(m, orbits=orbits)
    # TDI transfer function
    tdi_tf = tdi.compute_tdi_tf(f_subset, sgwb_cls.ltt, t_vect, gen="2.0")
    
    return f_subset, tdi_tf
                  

class TestNoises(unittest.TestCase):
    def test_component_model_fixed_basis(self, plot=False):

        # Characteristics of the data
        f_subset, tdi_tf = prepare_input()

        # Instantiate noise class
        noise_class = noise.NoiseModel(f_subset, noise.construct_component_basis,
                                       tdi_tf,
                                       basis_args=None,
                                       basis_kwargs={"noise_type":"OMS", "tm_relaxation": True},
                                       fixed_basis=True)

        # Compute arbitrary single-link PSD model
        theta_n = np.ones(3)
        sn = noise_class.compute_link_psd(theta_n)

        # knee_frequencies
        if plot:
            plt.figure(0)
            plt.loglog(f_subset, np.sqrt(sn))
            plt.savefig("noise_test_fixed_basis.pdf")
            
        assert not np.any(np.isnan(sn))
        
    def test_component_model_free_basis(self, plot=True):

        # Characteristics of the data
        f_subset, tdi_tf = prepare_input()

        # Instantiate noise class
        noise_class = noise.NoiseModel(f_subset, noise.construct_component_basis,
                                       tdi_tf,
                                       basis_args=4e-4,
                                       basis_kwargs={"noise_type":"OMS", "tm_relaxation": True},
                                       fixed_basis=False)

        # Compute arbitrary single-link PSD model
        coefficients = np.ones(3)
        theta_n = np.concatenate([coefficients, [4e-4]])
        sn = noise_class.compute_link_psd(theta_n)
        theta_n_2 = np.concatenate([coefficients, [1e-4]])
        sn_2 = noise_class.compute_link_psd(theta_n_2)

        # knee_frequencies
        if plot:
            plt.figure(0)
            plt.loglog(f_subset, np.sqrt(sn), label='fa3 = 4e-4')
            plt.loglog(f_subset, np.sqrt(sn_2), label='fa3 = 1e-4')
            plt.legend(loc='upper right')
            plt.savefig("noise_test_free_basis.pdf")
            
        assert not np.any(np.isnan(sn))


if __name__ == '__main__':

    unittest.main()
    # test_cls = TestNoises()
    # test_cls.test_component_model_fixed_basis(plot=True)
    
