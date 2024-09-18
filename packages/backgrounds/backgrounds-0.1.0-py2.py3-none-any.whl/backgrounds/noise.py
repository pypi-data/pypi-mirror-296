# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
import numpy as np
from scipy import interpolate
from . import utils, Response, tdi
from lisaconstants import SIDEREALYEAR_J2000DAY as YEAR_day
from lisaconstants import c

known_noise_config = ["Proposal", "SciRDv1", "MRDv1", "MRD_MFR",
                      "sangria", "spritz", "redbook"]
YEAR = YEAR_day * 24 * 3600
MOSAS = ['12', '23', '31', '13', '32', '21']


class GeneralNoiseModel(Response):
    """
    General mother class for noise models
    """

    def __init__(self, freq, t0, orbits, orbit_interp_order=1,
                 tdi_tf_func=tdi.compute_tdi_tf, gen="2.0", average=True, ltt=None):
        """
        Class constructor.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        t0 : ndarray or float
            time [s] at which the noise response is computed
        orbits : str
            orbit file path
        orbit_interp_order : int, optional
            order of the orbit interpolator, by default 1
        tdi_tf_func : callable, optional
            function yielding the TDI transfer function of the noise,
            by default tdi.compute_tdi_tf
        gen : str, optional
            TDI generation, by default "2.0"
        average : bool, optional
            If True, and if t0 is an array, computes the average of the TDI kernel matrix
            over all times. If False, compute_covariances will returns a 
            nf x nt x 3 x 3 array where the first dimension correspond to time samples.
        ltt : dictionary of callables
            light travel times. If None, they are computed from the orbit file. Default is None.

        """

        super().__init__(orbits, ltt=ltt, orbit_interp_order=orbit_interp_order,
                         tdi_tf_func=tdi_tf_func)

        self.freq = freq
        self.logfreq = np.log(self.freq)
        self.t0 = t0
        self.gen = gen
        self.average = average
        self.tdi_corr = []
        self.tdi_tf = self.compute_transfer_matrix(self.freq)
        # Dimension of the model
        self.ndim = 0

    def compute_transfer_matrix(self, freq):
        """
        Compute the transfer matrix to go from single-link measurements
        to TDI

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        """
        self.tdi_tf = self.tdi_tf_func(freq, self.ltt, self.t0, gen=self.gen)
        # Precompute quantities useful if equal, uncorrelated noises (nf x n_tdi x n_tdi) or
        # (nt x nf x n_tdi x n_tdi)
        if isinstance(self.t0, (np.ndarray, list)):
            self.tdi_corr = utils.multiple_dot(
                self.tdi_tf, np.swapaxes(self.tdi_tf.conj(), 2, 3))
            # Average the correlation matrix
            if self.average:
                self.tdi_corr = np.mean(self.tdi_corr, axis=1)
        else:
            self.tdi_corr = utils.multiple_dot(
                self.tdi_tf, np.swapaxes(self.tdi_tf.conj(), 1, 2))

        return self.tdi_tf

    def compute_link_psd(self, theta, freq=None, mosa='12', ffd=True):
        """
        Compute the single-link PSD

        Parameters
        ----------
        args : iterable
            psd model parameters
        kwargs : dictionary
            psd model keyword arguments

        Returns
        -------
        s_n : ndarray
            psd 
        """
        if freq is None:
            freq = self.freq
        return theta * np.ones_like(freq)

    def compute_link_log_psd(self, theta, freq=None, mosa='12', ffd=True):
        """
        Computes single-link log-PSDs.

        Parameters
        ----------
        theta : ndarray, optional
            model parameters, by default None
        freq : ndarray
            frequency array [Hz]
        mosa : str, optional
            MOSA indices, by default '12'
        ffd : bool, optional
            if True, returns the PSD in units of fractional frequency deviation, by default True

        Returns
        -------
        log_s_n : ndarray
           log-psd computed at all frequencies freq.
        """

        return np.log(self.compute_link_psd(theta, freq=freq, mosa=mosa, ffd=ffd))

    def compute_covariances(self, theta, freq=None, mosa='12', ffd=True):
        """
        Calculate the full covariances at frequencies finds.

        Parameters
        ----------
        theta : ndarray, optional
            model parameters, by default None
        freq : ndarray
            frequency array [Hz]
        mosa : str, optional
            MOSA indices, by default '12'
        ffd : bool, optional
            if True, returns the covariance in units of fractional frequency deviation,
            by default True

        Returns
        -------
        cov_tdi_n : ndarray
            matrix of covariances for all channels, size nf x 3 x 3 
            (if t0 is a float or average is True) or size nf x nt x 3 x 3
        """

        # Compute single-link PSD
        s_n = self.compute_link_psd(theta, freq=freq, mosa=mosa, ffd=ffd)
        # Apply TDI transfer matrix to the single-link PSDs
        if self.tdi_corr.ndim == 3:
            cov_tdi_n = self.tdi_corr * s_n[:, np.newaxis, np.newaxis]
        elif self.tdi_corr.ndim == 4:
            cov_tdi_n = self.tdi_corr * s_n[:, np.newaxis, np.newaxis, np.newaxis]

        return cov_tdi_n


class AnalyticOMSNoiseModel(GeneralNoiseModel):
    """
    General class to represent a single-link analytical OMS noise model
    """

    def __init__(self, freq, t0, orbits, orbit_interp_order=1, tdi_tf_func=tdi.compute_tdi_tf,
                 gen="2.0",
                 central_freq=281600000000000.0,
                 oms_isi_carrier_asds=7.9e-12,
                 oms_fknees=0.002, fs=None, duration=None, average=True, ltt=None):
        """
        Class constructor.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        t0 : float
            time [s] at which the noise response is computed
        orbits : str
            orbit file path
        orbit_interp_order : int, optional
            order of the orbit interpolator, by default 1
        gen : str, optional
            TDI generation, by default "2.0"
        central_freq : float, optional
            laser central frequency, by default 281600000000000.0
        isi_carrier_asds : float or dic, optional
            ASDs [unit/sqrt{Hz}] of the science interferometer noises, by default 7.9e-12
        fknees : float or dic, optional
            Knee frequencies [Hz] of the science interferometer noises, by default 0.002
        """

        super().__init__(freq, t0, orbits, orbit_interp_order=orbit_interp_order,
                         tdi_tf_func=tdi_tf_func, gen=gen, average=average, ltt=ltt)

        self.central_freq = central_freq
        self.ndim = 1
        self.fs = fs
        self.duration = duration

        if isinstance(oms_isi_carrier_asds, float):
            self.oms_isi_carrier_asds = {mosa: oms_isi_carrier_asds
                                         for mosa in MOSAS}
        if isinstance(oms_fknees, float):
            self.oms_fknees = {mosa: oms_fknees
                               for mosa in MOSAS}

    def compute_link_psd(self, theta, freq=None, mosa='12', ffd=True):
        """Model for OMS noise PSD in ISI carrier beatnote fluctuations.
        
        Parameters
        ----------
        theta : float
            Correction amplitude parameter. Applies a factor 10**theta 
            in front of the PSD model.
        freq : ndarray or float
            Frequencies [Hz] where to compute the PSD
        mosa : str
            MOSA index ij
        ffd : bool
            if ffd is True, returns the PSD in fractional frequency deviation

        Returns
        -------
        psd_hertz : PDD in Hz / Hz or /Hz

        """
        if freq is None:
            freq = self.freq

        asd = self.oms_isi_carrier_asds[mosa]
        fknee = self.oms_fknees[mosa]

        if (self.fs is None) | (self.duration is None):
            psd_meters = asd**2 * (1 + (fknee / freq) ** 4)
            psd_hertz = (2 * np.pi * freq * self.central_freq / c) ** 2 * psd_meters
        else:
            fmin = 1.0 / self.duration
            psd_highfreq = (asd * self.fs * self.central_freq / c) ** 2 * np.sin(
                2 * np.pi * freq / self.fs
            ) ** 2
            psd_lowfreq = (
                (2 * np.pi * asd * self.central_freq * fknee**2 / c) ** 2
                * np.abs(
                    (2 * np.pi * fmin)
                    / (
                        1
                        - np.exp(-2 * np.pi * fmin / self.fs)
                        * np.exp(-2j * np.pi * freq / self.fs)
                    )
                ) ** 2
                * 1 / (self.fs * fmin) ** 2
            )
            psd_hertz = psd_highfreq + psd_lowfreq

        if ffd:
            return 10**theta * psd_hertz/self.central_freq**2
        return 10**theta * psd_hertz
    
    def compute_ref_psd(self, freq):
        """Reference Model for OMS noise PSD in ISI carrier beatnote fluctuations.
        
        Parameters
        ----------
        freq : ndarray or float
            Frequencies [Hz] where to compute the PSD

        Returns
        -------
        psd_hertz : PDD in Hz / Hz or /Hz

        """
        
        return self.compute_link_psd(0.0, freq=freq, mosa='12', ffd=True)


class AnalyticTMNoiseModel(GeneralNoiseModel):
    """
    General class to represent a single-link analytical TM noise model
    """

    def __init__(self, freq, t0, orbits, orbit_interp_order=1, tdi_tf_func=tdi.compute_tdi_tf_tm,
                 gen="2.0",
                 central_freq=281600000000000.0,
                 tm_isi_carrier_asds=2.4e-15,
                 tm_fknees=0.0004, fs=None, duration=None, average=True, ltt=None):
        """
        Class constructor.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        t0 : float
            time [s] at which the noise response is computed
        orbits : str
            orbit file path
        orbit_interp_order : int, optional
            order of the orbit interpolator, by default 1
        gen : str, optional
            TDI generation, by default "2.0"
        central_freq : float, optional
            laser central frequency, by default 281600000000000.0
        isi_carrier_asds : float or dic, optional
            ASDs [unit/sqrt{Hz}] of the science interferometer noises, by default 7.9e-12
        fknees : float or dic, optional
            Knee frequencies [Hz] of the science interferometer noises, by default 0.002
        fs : float
            Sampling frequency (optional). If provided, it is used to compute the effect 
            of filters in the simulation.
        duration : float
            Observation duration (optional).
        """

        super().__init__(freq, t0, orbits, orbit_interp_order=orbit_interp_order,
                         tdi_tf_func=tdi_tf_func, gen=gen, average=average, ltt=ltt)

        self.central_freq = central_freq
        self.fs = fs
        self.duration = duration
        self.ndim = 1

        if isinstance(tm_isi_carrier_asds, float):
            self.testmass_asds = {mosa: tm_isi_carrier_asds
                                         for mosa in MOSAS}
        if isinstance(tm_fknees, float):
            self.testmass_fknees = {mosa: tm_fknees
                               for mosa in MOSAS}

    def compute_link_psd(self, theta, freq=None, mosa='12', ffd=True):
        """Model for OMS noise PSD in ISI carrier beatnote fluctuations.
        
        Parameters
        ----------
        freq : ndarray or float
            Frequencies [Hz] where to compute the PSD
        mosa : str
            MOSA index ij
        ffd : bool
            if ffd is True, returns the PSD in fractional frequency deviation


        Returns
        -------
        psd_hertz : PDD in Hz / Hz or /Hz

        """

        if freq is None:
            freq = self.freq

        asd = self.testmass_asds[mosa]
        fknee = self.testmass_fknees[mosa]

        if (self.fs is None) | (self.duration is None):
            psd_acc = asd**2 * (1 + (fknee / freq) ** 2)
            psd_hertz = (2 * self.central_freq / (2 * np.pi * c * freq)) ** 2 * psd_acc
        else:
            fmin = 1.0 / self.duration
            psd_highfreq = (
                (2 * asd * self.central_freq / (2 * np.pi * c)) ** 2
                * np.abs(
                    (2 * np.pi * fmin)
                    / (
                        1
                        - np.exp(-2 * np.pi * fmin / self.fs)
                        * np.exp(-2j * np.pi * freq / self.fs)
                    )
                )
                ** 2
                * 1
                / (self.fs * fmin) ** 2
            )
            psd_lowfreq = (
                (2 * asd * self.central_freq * fknee / (2 * np.pi * c)) ** 2
                * np.abs(
                    (2 * np.pi * fmin)
                    / (
                        1
                        - np.exp(-2 * np.pi * fmin / self.fs)
                        * np.exp(-2j * np.pi * freq / self.fs)
                    )
                )
                ** 2
                * 1
                / (self.fs * fmin) ** 2
                * np.abs(1 / (1 - np.exp(-2j * np.pi * freq / self.fs))) ** 2
                * (2 * np.pi / self.fs) ** 2
            )
            psd_hertz = psd_lowfreq + psd_highfreq

        if ffd:
            # The factor of 4 = 2^2 is to be consistent with backgrounds
            # conventions. The test-mass jitter noise vector is projected two times
            # onto the sensitive axis. The vector nij TM->OB:
            # beam = - 2 / c nij delta_ij
            return 10**theta * psd_hertz / (2*self.central_freq)**2
        return 10**theta * psd_hertz
    
    def compute_ref_psd(self, freq):
        """Reference Model for OMS noise PSD in ISI carrier beatnote fluctuations.
        
        Parameters
        ----------
        freq : ndarray or float
            Frequencies [Hz] where to compute the PSD

        Returns
        -------
        psd_hertz : PDD in Hz / Hz or /Hz

        """
        
        return self.compute_link_psd(0.0, freq=freq, mosa='12', ffd=True)   


class FunctionalNoiseModel(GeneralNoiseModel):
    """
    Noise model class implementing models where the log-PSD is an arbitrary function
    log PSD = f(theta).
    """

    def __init__(self, freq, t0, orbits, log_psd_func, log_psd_func_kwargs=None,
                 orbit_interp_order=1, ndim=0,
                 tdi_tf_func=tdi.compute_tdi_tf, gen="2.0",
                 ref_psd_func=None, average=True, ltt=None):
        """
        Class constructor.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        t0 : float
            time [s] at which the noise response is computed
        orbits : str
            orbit file path
        log_psd_func : callable
            function that computes the single-link PSDs as a function of frequency freq
            and parameters theta
        log_psd_func_kwargs : dictionary
            keyword arguments to pass to log_psd_func
        orbit_interp_order : int, optional
            order of the orbit interpolator, by default 1
        ndim : int, optional
            dimension of the noise parameters
        tdi_tf_func : callable, optional
            function yielding the TDI transfer function of the noise,
            by default tdi.compute_tdi_tf
        gen : str, optional
            TDI generation, by default "2.0"
        ref_psd_func : callable
            If provided, the model parameters describe deviations from a reference log-PSD, 
            which can be computed through ref_psd_func. Otherwise, they describe the log_psd itself.
        average : bool, optional
            If True, and if t0 is an array, computes the average of the TDI kernel matrix
            over all times. If False, compute_covariances will returns a 
            nf x nt x 3 x 3 array where the first dimension correspond to time samples.
        ltt : dictionary of callables
            light travel times. If None, they are computed from the orbit file. Default is None.
        """

        super().__init__(freq, t0, orbits, orbit_interp_order=orbit_interp_order,
                         tdi_tf_func=tdi_tf_func, gen=gen, average=average, ltt=ltt)

        # Log-PSD function describing the single-link model
        self.log_psd_func = log_psd_func
        # Basis keyword arguments
        if log_psd_func_kwargs is None:
            self.basis_kwargs = {}
        else:
            self.basis_kwargs = log_psd_func_kwargs
        # If we are describing deviations from a reference PSD
        self.ref_psd_func = ref_psd_func
        if ref_psd_func is not None:
            self.ref_log_psd = np.log(self.ref_psd_func(self.freq))
        else:
            self.ref_log_psd = 0
        # Dimension of the parameter space
        self.ndim = ndim

    def compute_link_psd(self, theta, freq=None, mosa='12', ffd=True):
        """
        Compute the single-link PSD

        Parameters
        ----------
        args : iterable
            psd model parameters
        kwargs : dictionary
            psd model keyword arguments

        Returns
        -------
        s_n : ndarray
            psd 
        """

        return np.exp(self.compute_link_log_psd(theta, freq=freq))

    def compute_link_log_psd(self, theta, freq=None):
        """
        Computes single-link log-PSDs.

        Parameters
        ----------
        theta : ndarray, optional
            model parameters, by default None
        freq : ndarray
            frequency array [Hz]
        mosa : str, optional
            MOSA indices, by default '12'
        ffd : bool, optional
            if True, returns the PSD in units of fractional frequency deviation, by default True

        Returns
        -------
        log_s_n : ndarray
           log-psd computed at all frequencies freq.
        """
        if freq is None:
            freq = self.freq
            ref_log_psd = self.ref_log_psd
        else:
            ref_log_psd = np.log(self.ref_psd_func(freq))
        return self.log_psd_func(freq, theta, **self.basis_kwargs) + ref_log_psd


class BasisNoiseModel(GeneralNoiseModel):
    """
    Noise model class implementing models where the log-PSD can be written as
    log PSD = A(theta) beta where A is a design matrix and beta a vector of coefficients (or 
    amplitudes). The design matrix A may depend on some parameters theta called `basis arguments`.
    """

    def __init__(self, freq, t0, orbits, basis_func, orbit_interp_order=1,
                 tdi_tf_func=tdi.compute_tdi_tf, gen="2.0", basis_args=None,
                 basis_kwargs=None, fixed_basis=True, ref_psd_func=None, average=True, ltt=None):
        """
        Class constructor.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        t0 : float
            time [s] at which the noise response is computed
        orbits : str
            orbit file path
        basis_func : callable
            function that construct the noise basis elements
        orbit_interp_order : int, optional
            order of the orbit interpolator, by default 1
        tdi_tf_func : callable, optional
            function yielding the TDI transfer function of the noise,
            by default tdi.compute_tdi_tf
        gen : str, optional
            TDI generation, by default "2.0"
        basis_args : iterable
            basis arguments.
        basis_kwargs : dictionary
            basis keyword arguments
        fixed_basis : bool
            If True, the basis is assumed to be fixed once for all. In that case, the parameters
            to compute the PSDs are only the amplitude coefficients. If False, then the parameters 
            will also include the arguments needed to compute the basis.
        ref_psd_func : callable
            If provided, the model parameters describe deviations from a reference log-PSD, 
            which can be computed through ref_psd_func. Otherwise, they describe the log_psd itself.
        average : bool, optional
            If True, and if t0 is an array, computes the average of the TDI kernel matrix
            over all times. If False, compute_covariances will returns a 
            nf x nt x 3 x 3 array where the first dimension correspond to time samples.
        ltt : dictionary of callables
            light travel times. If None, they are computed from the orbit file. Default is None.
        """

        super().__init__(freq, t0, orbits, orbit_interp_order=orbit_interp_order,
                         tdi_tf_func=tdi_tf_func, gen=gen, average=average, ltt=ltt)

        self.basis_func = basis_func
        self.fixed_basis = fixed_basis
        self.basis_args = basis_args
        # Basis keyword arguments
        if basis_kwargs is None:
            self.basis_kwargs = {}
        else:
            self.basis_kwargs = basis_kwargs
        self.x_mat = self.compute_design_matrix(basis_args=self.basis_args)
        self.projector = self.compute_projector()
        self.n_coeffs = self.x_mat.shape[1]

        # If the design matrix if fixed once for all
        self.ndim = int(self.n_coeffs)
        if not self.fixed_basis:
            self.ndim += np.atleast_1d(basis_args).size
        # If we are describing deviations from a reference PSD
        self.ref_psd_func = ref_psd_func
        if ref_psd_func is not None:
            self.ref_log_psd = np.log(self.ref_psd_func(self.freq))
        else:
            self.ref_log_psd = 0

    def compute_design_matrix(self, freq=None, basis_args=None):
        """
        Construct the design matrix from frequencies and non-linear parameters.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        basis_args : iterable, optional
            Parameter arguments to contruct the basis, by default None. For a spline basis,
            it will be the interior knots locations.

        Returns
        -------
        x_mat : ndarray
            design matrix
        """

        if freq is None:
            logfreq = self.logfreq
        else:
            logfreq = np.log(freq)

        if basis_args is None:
            return self.basis_func(logfreq, **self.basis_kwargs)
        else:
            return self.basis_func(logfreq, basis_args, **self.basis_kwargs)

    def compute_link_log_psd(self, theta, freq=None, mosa='12', ffd=True):
        """
        Computes single-link log-PSDs.

        Parameters
        ----------
        theta : ndarray, optional
            model parameters, by default None
        freq : ndarray
            frequency array [Hz]
        mosa : str, optional
            MOSA indices, by default '12'
        ffd : bool, optional
            if True, returns the PSD in units of fractional frequency deviation, by default True

        Returns
        -------
        log_s_n : ndarray
           log-psd computed at all frequencies freq.
        """
        # If the basis is fixed
        if (freq is None) & (self.fixed_basis):
            x_mat = self.x_mat
            coefficients = theta
        elif (freq is not None) & (self.fixed_basis):
            x_mat = self.compute_design_matrix(freq=freq)
            coefficients = theta
        else:
            # If the basis is not fixed
            coefficients = theta[0:self.n_coeffs]
            basis_args = theta[self.n_coeffs:]
            x_mat = self.compute_design_matrix(freq=freq, basis_args=basis_args)

        return x_mat.dot(coefficients) + self.ref_log_psd

    def compute_link_psd(self, theta, freq=None, mosa='12', ffd=True):
        """
        Computes single-link PSDs.

        Parameters
        ----------
        theta : ndarray, optional
            model parameters, by default None
        freq : ndarray
            frequency array [Hz]
        mosa : str, optional
            MOSA indices, by default '12'
        ffd : bool, optional
            if True, returns the PSD in units of fractional frequency deviation, by default True

        Returns
        -------
        log_s_n : ndarray
           log-psd computed at all frequencies freq.
        """

        return np.exp(self.compute_link_log_psd(theta, freq=freq, mosa=mosa, ffd=ffd))

    def compute_projector(self, x_mat=None):
        """Pre-compute the matrix (A^TA)^{-1}A^T

        Parameters
        ----------
        x_mat : ndarray, optional
            design matrix, by default None

        Returns
        -------
        p_mat : ndarray
            least square projector matrix.
        """

        if x_mat is None:
            x_mat = self.x_mat

        return np.linalg.pinv(x_mat.T.dot(x_mat)).dot(x_mat.T)

    def fit(self, data):
        """
        Performs a least-square fit of the model coefficients.

        Parameters
        ----------
        data : ndarray
            data array

        Returns
        -------
        beta : ndarray
            least square estimator of the model coefficents.
        """
        return self.projector.dot(data)

    def estimate(self, data):
        """
        Compute the predictive value of the log-PSD from the least-square fit of the model
        coefficients.

        Parameters
        ----------
        data : ndarray
            data array

        Returns
        -------
        log_psd : ndarray
            least square estimate of the log-PSD
        """
        theta = self.fit(data)
        return self.x_mat.dot(theta)


class AnalyticNoiseModel(GeneralNoiseModel):
    """
    General class defining an analytic noise model from its TDI transfer function.

    """

    def __init__(self, freq, t0, orbits, link_psd_func,
                 orbit_interp_order=1,
                 tdi_tf_func=tdi.compute_tdi_tf, gen="2.0", ndim=0, average=True, ltt=None):
        """

        Parameters
        ----------
        freq : ndarray
            frequency array
        basis_func : callable
            function that computes the noise transfer function from 
            single-links to TDI
        link_psd_func : callable
            Function that computes the single-link PSD as a function of frequency
        ndim : int
            Dimension of the model
        
        """

        super().__init__(freq, t0, orbits, orbit_interp_order=orbit_interp_order,
                         tdi_tf_func=tdi_tf_func, gen=gen, average=average, ltt=ltt)
        
        # Store the single-link PSD function
        self.link_psd_func = link_psd_func
        # Get only the diagonal element of the correlation matrix
        self.tdi_coeff = np.array([self.tdi_corr[:, i, i]
                                   for i in range(self.tdi_corr.shape[1])]).T
        # Change dimension if needed (it should be zero, though, since there are no parameters)
        self.ndim = ndim

    def compute_link_psd(self, freq):
        """
        Compute the single-link noise PSD
        evaluated at parameter theta.

        Parameters
        ----------
        freq : ndarray
            frequency array where to compute the PSD, if different
            from self.freq

        Returns
        -------
        psd : ndarray
            Single-link PSD computed at frequencies freq.
        """

        return self.link_psd_func(freq)

    def compute_link_logpsd(self, freq):
        """
        Compute the single-link log-PSD from the noise parameters.

        Parameters
        ----------
        freq : ndarray or None
            Frequencies where to compute the single-link PSD. If None, the
            PSD is computed at the domain frequencies.

        Returns
        -------
        s_n : ndarray
            log-psd computed at all frequencies freq.
        """

        return np.log(self.compute_link_psd(freq))

    def compute_covariances(self, freq):
        """
        Calculate the full covariances at frequencies freq.

        Parameters
        ----------
        freq : ndarray or None
            Frequencies where to compute the single-link PSD. If None, the
            PSD is computed at the domain frequencies.

        Returns
        -------
        cov_tdi_n : ndarray
            matrix of covariances for all channels, size nf x 3 x 3
        """

        # Compute single-link PSD
        s_n = self.compute_link_psd(freq)
        if self.tdi_corr.shape[0] != freq.size:
            self.tdi_tf = self.compute_transfer_matrix(freq)
            self.tdi_corr = utils.multiple_dot(
                self.tdi_tf, np.swapaxes(self.tdi_tf.conj(), 1, 2))
        # Apply TDI transfer matrix to the single-link PSDs
        cov_tdi_n = self.tdi_corr * s_n[:, np.newaxis, np.newaxis]

        return cov_tdi_n

    def compute_logpsds(self, freq):
        """
        Calculate the log-PSD at frequencies freq.

        Parameters
        ----------
        freq : ndarray or None
            Frequencies where to compute the single-link PSD. If None, the
            PSD is computed at the domain frequencies.
    
        Returns
        -------
        logsn_tdi : ndarray
            vector of log-PSDs for all channels, size nf x 3
        """

        logs_n = self.compute_link_logpsd(freq)
        if self.tdi_corr.shape[0] != freq.size:
            self.tdi_tf = self.compute_transfer_matrix(freq)
            self.tdi_coeff = np.array([self.tdi_corr[:, i, i]
                                       for i in range(self.tdi_corr.shape[1])]).T
        # Apply TDI transfer function to the single-link PSDs
        logsn_tdi = np.log(self.tdi_coeff) + logs_n[:, np.newaxis]

        return logsn_tdi


class SplineNoiseModel(FunctionalNoiseModel):
    """
    Class constructing a noise model with a spline describing the
    single-link measurement noise PSD. Assumes orthogonal TDI
    """

    def __init__(self, freq, t0, orbits,
                 orbit_interp_order=1,
                 tdi_tf_func=tdi.compute_tdi_tf, gen="2.0", ref_psd_func=None,
                 average=True, ltt=None,
                 n_coeffs=5,
                 fixed_knots=False, f_knots=None, spline_type="bsplines", degree=3):
        """
        Likelihood with noise-only model.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        t0 : float
            time [s] at which the noise response is computed
        orbits : str
            orbit file path
        orbit_interp_order : int, optional
            order of the orbit interpolator, by default 1
        tdi_tf_func : callable, optional
            function yielding the TDI transfer function of the noise,
            by default tdi.compute_tdi_tf
        gen : str, optional
            TDI generation, by default "2.0"
        ref_psd_func : callable
            If provided, the model parameters describe deviations from a reference log-PSD, 
            which can be computed through ref_psd_func. Otherwise, they describe the log_psd itself.
        average : bool, optional
            If True, and if t0 is an array, computes the average of the TDI kernel matrix
            over all times. If False, compute_covariances will returns a 
            nf x nt x 3 x 3 array where the first dimension correspond to time samples.
        ltt : dictionary of callables
            light travel times. If None, they are computed from the orbit file. Default is None.
        n_coeffs : int
            Number of spline coefficients
        f_knots : ndarray
            initial interior knots
        fixed_knots : bool
            if True, the knot locations are fixed. Default is False.
        f_knots : ndarray or None
            Spline interior knot frequencies. Used only if fixed_knots is False.
        spline_type : str
            Type of splines between {bsplines, akimasplines}
        degree : int
            degree of spline

        """

        # Number of spline coefficients
        self.n_coeffs = n_coeffs
        self.x_min = np.log(freq[0])
        self.x_max = np.log(freq[-1])
        self.spline_type = spline_type
        self.degree = degree
        self.kind = utils.order2kind(degree)
        # Fixed knots flag
        self.fixed_knots = fixed_knots
        # Spline interior knot frequencies if provided
        self.f_knots = f_knots
        if self.f_knots is not None:
            self.logf_knots = np.log(f_knots)
        else:
            self.logf_knots = None
        # Number of parameters to fit
        if not fixed_knots:
            ndim = 2*self.n_coeffs - 2
        else:
            ndim = self.n_coeffs

        super().__init__(freq, t0, orbits, self.log_psd, log_psd_func_kwargs=None,
                         orbit_interp_order=orbit_interp_order, ndim=ndim,
                         tdi_tf_func=tdi_tf_func, gen=gen,
                         ref_psd_func=ref_psd_func, average=average, ltt=ltt)

    def log_psd(self, freq, theta):
        """
        Function computing the log PSD with splines.

        Parameters
        ----------
        freq : ndarray
            frequency array [Hz]
        theta : ndarray
            vector of parameters, including spline coefficients and spline locations
            (if fixed_knots is False)

        Returns
        -------
        ndarray
            log-PSD computed at the frequencies freq.
        """

        y_knots = theta[0:self.n_coeffs]
        if self.fixed_knots:
            x_knots = np.concatenate([[self.x_min],
                                    self.logf_knots,
                                    [self.x_max]])
        else:
            x_knots = np.concatenate([[self.x_min],
                                    theta[self.n_coeffs:],
                                    [self.x_max]])
        if self.spline_type == "akimasplines":
            spline_func = interpolate.Akima1DInterpolator(x_knots, y_knots, axis=-1)
        elif self.spline_type == "bsplines":
            spline_func = interpolate.interp1d(x_knots, y_knots,
                                              kind=self.kind,
                                              axis=-1,
                                              copy=True,
                                              bounds_error=False,
                                              fill_value="extrapolate")

        return spline_func(np.log(freq))

    def compute_design_matrix(self, freq=None, basis_args=None):
        """
        Computation of the spline design matrix.

        Parameters
        ----------
        freq : ndarray or None
            frequencies where to compute the design matrix.
            if None, use the frequencies provided when 
            instantiating the class.
        intknots : ndarray
            parameters for interior knots locations (log-frequencies)

        Returns
        -------
        ndarray
            design matrix A such that the PSD can be written A.dot(coeffs)
        """

        if basis_args is None:
            intknots = self.logf_knots[1:-1]
        else:
            intknots = basis_args

        if self.hypertriangle:
            # Re-order the knot location parameters by hypertriangulation
            x_knots = utils.hypertriangulate(
                intknots, bounds=(self.logfreq[0], self.logfreq[-1]))
        else:
            x_knots = intknots[:]
        # # Recontruct knot vector
        # Add boundaries of the domain to the interior knots
        knots_list = [self.logfreq[0]] + list(x_knots) + [self.logfreq[-1]]
        logf_knots = np.asarray(knots_list)
        # Change the data and reset the spline class
        if self.spline_type == "bsplines":
            basis_func = interpolate.interp1d(logf_knots, np.eye(self.n_coeffs),
                                              kind=self.kind,
                                              axis=-1,
                                              copy=True,
                                              bounds_error=False,
                                              fill_value="extrapolate",
                                              assume_sorted=self.hypertriangle)
        elif self.spline_type == "akimasplines":
            basis_func = interpolate.Akima1DInterpolator(logf_knots,
                                                         np.eye(self.n_coeffs),
                                                         axis=-1)

        if freq is None:
            return basis_func(self.logfreq).T
        else:
            return basis_func(np.log(freq)).T


class LinkNoiseModel(object):

    def __init__(self):
        """
        Class defining LISA's noise models

        Returns
        -------
        None.
            Instantiate the class.

        """

        # Laser absolute frequency stability [Hz/sqrt(Hz)]
        self.a0 = 28.2
        # Laser central frequency
        self.c_light = 299792458.0
        self.nu0 = self.c_light/1064e-9
        # TM displacement noise amplitude spectral density [m/s2]
        self.atm = 3e-15
        # OMS constant amplitude spectral density in displacement [m]
        self.aoms = 15e-12
        # Acceleration knee frequency
        self.fa1 = 4e-4
        # Acceleration positive slope frequency
        self.fa2 = 8e-3
        # OMS noise knee frequency
        self.fa3 = 2e-3
        # Low-frequency cut-off to avoid outflows
        self.f_low_cut = 1e-6
        # Read-out noise levels for all channels
        self.phi_ro_s = 6.1e-5  # Cf. Markus Otto's thesis.
        self.phi_ro_e = 2.4e-7
        # self.phi_ro_t = 4.4e-8
        self.phi_ro_t = 6.1e-5
        # OMS spectral density for reference interferometer in displacement [m]
        self.aoms_t = 3.32e-12  # Cf. LISANode

    def freq_noise_model(self, f, fknee=0):
        """

        PSD of laser frequency noise converted in fractional frequency
        in 1/Hz

        Parameters
        ----------
        f : array_like
            frequency in Hz

        Returns
        -------
        s : array_like
            laser frequency noise PSD in fractional frequency (1/Hz)

        Reference
        ---------
        [1] O. Jennrich, LISA technology and instrumentation, 2009
        https://arxiv.org/pdf/0906.2901.pdf
        Cf. also LISANode:
        [2] LISA Performance Model and Error Budget. LISA-LCST-INST-TN-003
        (Jun. 2018).
        [3] Thompson, R., et al., A flight-like optical reference cavity for
        GRACE follow-on laser frequency stabilization. 2011, Joint Conference
        on the IEEE International.

        """

        s_freq = self.a0**2

        if fknee == 0:
            freqcolor = np.ones(len(f))
        else:
            freqcolor = (fknee / f) ** 4

        return s_freq*(1/self.nu0)**2 * freqcolor

    def readout_noise_model(self, f, channel='reference'):
        """
        Term modeling shot noise, relative intensity and electronic readout 
        noise.
        See M. Otto PhD Thesis, Eq. (2.25)
        See also p.51 for readout noise levels.

        Parameters
        ----------
        f : array_like
            frequency in Hz
        channel : str, optional
            Interferometer type, by default 'reference'


        Reference
        ---------
        Markus Otto, PhD thesis, 2015.

        """

        if channel == 'reference':
            phi = self.phi_ro_t
            n_ro = (2 * np.pi / self.c_light * self.aoms_t * f)**2
        elif channel == 'science':
            phi = self.phi_ro_s
            n_ro = (phi * f / (2 * np.pi * self.nu0))**2
        elif channel == 'test-mass':
            phi = self.phi_ro_e
            n_ro = (phi * f / (2 * np.pi * self.nu0))**2

        return n_ro

    def acceleration_noise_model(self, f, atm=None):
        """

        PSD of Acceleration noises converted in fractional frequency
        in 1/Hz

        [1] LISA Performance Model and Error Budget. LISA-LCST-INST-TN-003
        (Jun. 2018).

        """

        atm_to_use = np.atleast_1d(atm) if atm is not None else np.atleast_1d(self.atm)
        # TM acceleration noise [(m/s2)^2/Hz]
        sa = atm_to_use[:,None] ** 2 * (1 + (self.fa1 / (f + self.f_low_cut))**2)
        sa *= (1 + ((f + self.f_low_cut)/self.fa2)**4)
        # Convert into relative frequency
        sa /= (2 * np.pi * (f + self.f_low_cut) * self.c_light) ** 2
        return sa.squeeze()

    def oms_noise_model(self, f, aoms=None):
        """

        PSD of OMS noises converted in fractional frequency
        in 1/Hz

        OMS includes optical path noises and readout noises

        [1] LISA Performance Model and Error Budget. LISA-LCST-INST-TN-003
        (Jun. 2018).

        """
        aoms_to_use = np.atleast_1d(aoms) if aoms is not None else np.atleast_1d(self.aoms)
        # Optical metrology system noise
        so = (aoms_to_use[:,None])**2 * (1 + (self.fa3/(f + self.f_low_cut))**4)
        # Convert in relative frequency units
        so *= (2.0 * np.pi * (f + self.f_low_cut) / self.c_light)**2
        return so.squeeze()

    def other_noise_model(self, f):
        """

        PSD of other measurement noises converted in fractional frequency
        in 1/Hz

        [1] LISA Performance Model and Error Budget. LISA-LCST-INST-TN-003
        (Jun. 2018).

        """
        # TM acceleration noise [(m/s2)^2/Hz]
        sa = self.acceleration_noise_model(f)
        # Optical metrology system noise
        so = self.oms_noise_model(f)

        return 2 * sa + so

    def other_noise_model_fit(self, f, logatm=np.log10(3e-15), logaoms=np.log10(15e-12)):
        """

        PSD of other measurement noises converted in fractional frequency
        in 1/Hz

        This function can be used for fitting with multiple temperatures and 
        walkers. 

        [1] LISA Performance Model and Error Budget. LISA-LCST-INST-TN-003
        (Jun. 2018).

        """
        # TM displacement noise amplitude spectral density [m/s2]
        self.atm = 10**logatm
        # OMS constant amplitude spectral density in displacement [m]
        self.aoms = 10**logaoms

        # TM acceleration noise [(m/s2)^2/Hz]
        sa = self.acceleration_noise_model(f)
        # Optical metrology system noise
        so = self.oms_noise_model(f)

        return 2 * sa + so


def generate_single_link_noises(ns, fs, central_freq=281600000000000.0,
                                links=['12', '23', '31', '13', '32', '21']):

    noise_model = LinkNoiseModel()
    instrument_psd = noise_model.other_noise_model
    measurements_noise = {}
    # Science, Reference and test-mass interferometers
    for link in links:
        measurements_noise[f'isc_{link}'] = utils.generate_noise(
            instrument_psd, ns, fs)[0:ns].real*central_freq
        measurements_noise[f'ref_{link}'] = np.zeros(
            measurements_noise[f'isc_{link}'].shape[0])
        measurements_noise[f'tm_{link}'] = np.zeros(
            measurements_noise[f'isc_{link}'].shape[0])

    return measurements_noise


class GalacticNoise(object):

    def __init__(self, freq, Tobs, snr=7.0, links=6, armlength=2.5e9, tdi_var='xyz'):

        self.freq = freq
        self.Tobs = Tobs
        self.Tobs_yrs = Tobs / YEAR
        self.arm_length = armlength
        self.ndim = 1
        self.tdi_var = tdi_var
        self.set_galactic_pars(snr=snr, links=links)

    def set_galactic_pars(self, snr=7.0, links=6):
        """
        From Mauro's code.
        """

        Tmin = 0.25
        Tmax = 10.0

        if snr not in [5.0, 7.0]:
            print('We accept SNR to be 5 or 7', 'given', snr)
            raise NotImplementedError
        if links not in [6, 4]:
            print('We accept links to be 4 or 6', 'given', links)
            raise NotImplementedError

        L6_snr5 = [1.14e-44, 1.66, 0.00059, -0.15, -2.78, -0.34, -2.55]
        L6_snr7 = [1.15e-44, 1.56, 0.00067, -0.15, -2.72, -0.37, -2.49]

        if snr == 5 and links == 6:
            self.Ampl, self.alpha, self.fr2, self.af1, self.bf1, self.afk, self.bfk = L6_snr5
        elif snr == 5 and links == 4:
            raise ValueError('Cannot accept 4 links')
            #Ampl, alpha, fr2, af1, bf1, afk, bfk    = L4_snr5
        elif snr == 7 and links == 6:
            self.Ampl, self.alpha, self.fr2, self.af1, self.bf1, self.afk, self.bfk = L6_snr7
        elif snr == 7 and links == 4:
            raise ValueError('Cannot accept 4 links')
            #Ampl, alpha, fr2, af1, bf1, afk, bfk    = L4_snr7

        if (self.Tobs_yrs < Tmin or self.Tobs_yrs > Tmax):
            print('Galaxy fit is valid between 3 months and 10 years')
            print('we do not extrapolate', self.Tobs_yrs, ' not in', Tmin, Tmax)
            raise NotImplementedError("")

        self.fr1 = 10.**(self.af1 * np.log10(self.Tobs_yrs) + self.bf1)
        self.frk = 10.**(self.afk * np.log10(self.Tobs_yrs) + self.bfk)

        # return Ampl, alpha, fr1, frk, fr2

    def compute_covariances(self, params, tdi2=False, freq=None):
        """
        Evaluate the model at parameters values for all 
        frequencies
        """

        if freq is None:
            freq = self.freq

        lisaLT = self.arm_length/c
        x = 2.0 * np.pi * lisaLT * freq
        t = 4.0 * x**2 * np.sin(x)**2

        Ampl = 10**params
        Sg_sens = Ampl*np.exp(-(self.freq/self.fr1)**self.alpha) *\
            (self.freq**(-7./3.))*0.5 * \
            (1.0 + np.tanh(-(self.freq-self.frk)/self.fr2))

        # For XX
        s_xx = t*Sg_sens
        # For XY
        s_xy = -0.5*s_xx
        if tdi2:
            factor_tdi2 = 4 * np.sin(2 * x)**2
            s_xx *= factor_tdi2
            s_xy *= factor_tdi2

        if self.tdi_var == 'aet':
            # cov_gal = utils.transform_covariance(tdi.aet_mat[np.newaxis, :, :], cov_gal)
            # cov_gal = np.asarray([cov_gal[:, i, i] for i in range(cov_gal.shape[1])]).T
            cov_gal = np.asarray(
                [1.5 * s_xx, 1.5 * s_xx, np.zeros(freq.size)]).T
        else:
            # Create a 3 x 3 x nf array
            cov_gal = np.asarray([[s_xx, s_xy, s_xy],
                                  [s_xy.conj(), s_xx, s_xy],
                                  [s_xy.conj(), s_xy.conj(), s_xx]])

            cov_gal = np.swapaxes(cov_gal.T, 1, 2)

        return cov_gal


def epanechnikov(x):
    kernel = np.zeros_like(x)
    y = 3/4 * (1 - x**2)
    kernel[y >= 0] = y[y >= 0]

    return kernel


def gauss(x):

    return np.exp(-x**2/2) / np.sqrt((2*np.pi))


def natural_basis_func(u):
    b = np.zeros_like(u)
    b[u >= 0] = u[u >= 0]**3
    return b


def construct_spline_basis(x, x_knots, degree=3, splinetype="bsplines", add_ext_knots=False):
    """
    Construct a basis of B-splines given log-frequencies x
    and a number of knot coefficients n_coeffs
    
    Parameters
    ----------
    x : ndarray
        data abscissa like log-frequencies
    x_knots : ndarray
        knots abscissa like log-knot frequencies (including exterior)
    degree : int
        spline degree
    splinetype : str
        type of spline among {"bsplines", "naturalspines", "akimasplines"}
    add_ext_knots : bool
        if True, it will append the extrema values of x to the interior knots x_knots to build
        the spline basis. Default is False.

    Returns
    -------
    x_mat : ndarray
        spline design matrix of shape (x.size, x_knots.size)
    
    """

    # If we include exterior points
    if add_ext_knots:
        y = np.concatenate([[x[0]], np.asarray(x_knots), [x[-1]]])
    else:
        y = x_knots[:]

    if splinetype == "bsplines":
        # Order of the spline
        kind = utils.order2kind(degree)
        basis_func = interpolate.interp1d(y, np.eye(y.size),
                                          kind=kind,
                                          axis=-1,
                                          copy=True,
                                          bounds_error=False,
                                          fill_value="extrapolate")
        # Spline design matrix
        x_mat = basis_func(x).T
    elif ((splinetype == "naturalsplines") | (splinetype == "NaturalSplines")) and (degree == 3):
        basis_list = [x**i for i in range(4)]
        basis_list = basis_list + [natural_basis_func(x-xk) for xk in y]
        x_mat = np.asarray(basis_list).T
    elif splinetype == "akimasplines":
        basis_func = interpolate.Akima1DInterpolator(y,
                                                     np.eye(y.size),
                                                     axis=-1)
        x_mat = basis_func(x).T
    else:
        raise NotImplementedError(
            'Natural spline basis with degree different than 3 not implemented')

    return x_mat


def construct_component_basis(x, knee_frequencies=None, noise_type="OMS", tm_relaxation=False):
    """
    Construct a basis of frequency-dependent components.

    Parameters
    ----------
    x : ndarray
        abscissa where to compute the basis. Like log-frequencies.
    knee_frequencies : ndarray
        Vector of knee frequencies. If noise_type is 'TM', contains the TM knee frequencies fa1 and 
        fa2. If noise_type is 'OMS', contains the knee frequency fa1.
    noise_type : str
        Type of noise among {'TM', 'OMS'}
    tm_relaxation : bool
        Wether to include the term in 1 + (freq/fa2)**4 in the TM noise.
    
    """

    # Assume that x = log(f)
    freq = np.exp(x)

    if noise_type == "OMS":
        if knee_frequencies is None:
            fa3 = 2e-3
        else:
            fa3 = knee_frequencies

        x_mat_list = [np.ones(x.size), x, np.log(1+(fa3/freq)**4)]

    elif noise_type == "TM":
        if knee_frequencies is None:
            fa1 = 4e-4
            fa2 = 8e-3
        elif (knee_frequencies is not None) & (tm_relaxation):
            fa1 = knee_frequencies[0]
            fa2 = knee_frequencies[1]
        elif (knee_frequencies is not None) & (not tm_relaxation):
            fa1 = knee_frequencies

        x_mat_list = [np.ones(x.size), x, np.log(1 + (fa1/freq)**2)]
        if tm_relaxation:
            x_mat_list.append(np.log(1 + (freq/fa2)**4))

    return np.asarray(x_mat_list).T


def construct_weighted_poly_basis(x, x_knots, bandwidths, degree=3,
                                  ker_func=gauss, output_kernel=False):
    """
    Construct basis of weighted (local) polynomials
    """

    design_mat = []
    kernel_mat = []

    for i in range(x_knots.size):
        ker = ker_func((x-x_knots[i])/bandwidths[i])/bandwidths[i]
        for j in range(degree+1):
            design_mat.append((x-x_knots[i])**j * ker)
            kernel_mat.append(ker)

    if output_kernel:
        return np.asarray(design_mat).T, np.asarray(kernel_mat).T
    return np.asarray(design_mat).T


class Splines:

    def __init__(self, finds, n_coeffs, splinetype='akimasplines', degree=3):

        self.finds = finds
        self.n_coeffs = n_coeffs
        self.x_min = np.log(finds[0])
        self.x_max = np.log(finds[-1])
        self.splinetype = splinetype
        self.degree = degree
        self.kind = utils.order2kind(degree)

    def log_psd(self, freq, theta):
        
        y_knots = theta[0:self.n_coeffs]
        x_knots = np.concatenate([[self.x_min],
                                  theta[self.n_coeffs:],
                                  [self.x_max]])
        if self.splinetype == "akimasplines":
            spline_func = interpolate.Akima1DInterpolator(x_knots, y_knots, axis=-1)
        elif self.splinetype == "bsplines":
            spline_func = interpolate.interp1d(x_knots, y_knots,
                                              kind=self.kind,
                                              axis=-1,
                                              copy=True,
                                              bounds_error=False,
                                              fill_value="extrapolate")

        return spline_func(np.log(freq))


class AnalyticNoise:
    """
    Class reproducing LDC noise model
    """


    psd_oms_d = {'Proposal':(10.e-12)**2, 'SciRDv1':(15.e-12)**2,
                 'MRDv1':(10.e-12)**2, 'MRD_MFR':(13.5e-12)**2,
                 'sangria':(7.9e-12)**2, 'spritz':(7.9e-12)**2}  # m^2/Hz
    psd_a_a = {'Proposal':(3.e-15)**2, 'SciRDv1':(3.e-15)**2,
               'MRDv1':(2.4e-15)**2,'MRD_MFR':(2.7e-15)**2,
               'sangria':(2.4e-15)**2, 'spritz':(2.4e-15)**2} # m^2/sec^4/Hz
    psd_mu_d = {'Proposal':0, 'SciRDv1':0,
                'MRDv1':0,'MRD_MFR':0,
                'sangria':0, 'spritz':(3e-12)**2} # m^2/Hz

    @staticmethod
    def set_noise_model(name, oms=(15.e-12)**2, acc=(3.e-15)**2, mu=0):
        """ Add custom noise model to the list of known config. 

        >>> AnalyticNoise.set_noise_model("my_noise")
        >>> f = np.logspace(-5, 0, 1000)
        >>> N = AnalyticNoise(f, model="my_noise")
        """
        err_msg = f"choose a dedicated name for your custom noise "\
            f"(not in {known_noise_config})"
        assert name not in known_noise_config, err_msg
        AnalyticNoise.psd_oms_d[name] = oms
        AnalyticNoise.psd_a_a[name] = acc
        AnalyticNoise.psd_mu_d[name] = mu

    def __init__(self, frq, model="SciRDv1", wd=0):

        self.freq = frq
        self.wd = wd
        self.model = model
        self.oms_relaxation = model != 'spritz'
        self.set_freq(frq)

    def set_freq(self, frq):
        """Set frequency array and compute the phasemeter
        TM and OMS noises

        Parameters
        ----------
        frq : ndarray
            frequency array
        """

        self.freq = frq

        # Acceleration noise
        sa_a = AnalyticNoise.psd_a_a[self.model] * (1.0 +(0.4e-3/frq)**2) *\
               (1.0+(frq/8e-3)**4) # in acceleration
        self.sa_d = sa_a*(2.*np.pi*frq)**(-4.) # in displacement
        sa_nu = self.sa_d*(2.0*np.pi*frq/c)**2 # in rel freq unit
        self.s_pm = sa_nu

        # Optical Metrology System
        relax = (1. + (2.e-3/frq)**4) if self.oms_relaxation else 1.0
        self.psd_oms_d = AnalyticNoise.psd_oms_d[self.model] * relax # in displacement
        s_oms_nu = self.psd_oms_d*(2.0*np.pi*frq/c)**2 # in rel freq unit
        self.s_op =  s_oms_nu

        # Backlink
        self.s_mu = AnalyticNoise.psd_mu_d[self.model] * (1. + (2.e-3/frq)**4)
        # Convert into fractional frequency
        self.s_mu *= (2 * np.pi * frq / c) ** 2

    def relative_freq(self):
        """ Return acceleration and OMS noise in relative freq unit
        """
        return self.s_pm, self.s_op

    def link_model_func(self, frq=None):

        if frq is not None:
            self.set_freq(frq)

        s_pm, s_op = self.relative_freq()

        return 2 * s_pm + s_op

    def acceleration_noise_model(self, frq):
        """Set frequency array and compute the phasemeter
        TM and OMS noises

        Parameters
        ----------
        frq : ndarray
            frequency array
        """

        # Acceleration noise
        sa_a = AnalyticNoise.psd_a_a[self.model] * (1.0 +(0.4e-3/frq)**2) *\
               (1.0+(frq/8e-3)**4) # in acceleration
        sa_d = sa_a*(2.*np.pi*frq)**(-4.) # in displacement
        sa_nu = sa_d*(2.0*np.pi*frq/c)**2 # in rel freq unit

        return sa_nu

    def oms_noise_model(self, frq):

        # Optical Metrology System
        relax = (1. + (2.e-3/frq)**4) if self.oms_relaxation else 1.0
        psd_oms_d = AnalyticNoise.psd_oms_d[self.model] * relax # in displacement
        s_oms_nu = psd_oms_d*(2.0*np.pi*frq/c)**2 # in rel freq unit

        return s_oms_nu

    def backlink_noise_model(self, frq):

        # Backlink
        s_mu = AnalyticNoise.psd_mu_d[self.model] * (1. + (2.e-3/frq)**4)
        # Convert into fractional frequency
        s_mu *= (2 * np.pi * frq / c) ** 2

        return s_mu
