# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
import warnings
import numpy as np
from scipy import interpolate
from . import utils


class TDICovarianceLikelihood:
    """
    Class implementing the Wishart likelihood in the frequency domain
    """

    def __init__(self, freqs, wper, instr, sgwb, k_seg, times=None, inf=1e14):
        """
        Gaussian likelihood model the full XYZ Welch spectrum matrix.

        Parameters
        ----------
        freqs : ndarray
            Vector of frequencies
        wper : ndarray
            Periodogram matrix at frequencies `freqs`, size nf x 3 x 3
        instr : NoisePSD instance or list
            class to compute the instrumental PSD (or list of classes)
        sgwb : SignalPSD instance or list
            class to compute the SGWB PSD (or list of classes)
        k_seg : int
            effective number of degrees of freedom. It can be the number of segments used for the
            Welch averaging if we assume the complex Wishart distribution.
        times : ndarray or None
            vector of time samples for time-frequency analysis. By default, None.
        inf : float or np.inf
            if the likelihood diverge, it will be set equal to - inf

        """

        self.freqs = freqs
        self.times = times
        # If we have a time dimension, let's merge it with frequency.
        if wper.ndim == 4:
            self.nt, self.nf, self.p, _ = np.shape(wper)
            self.wper = np.reshape(wper, (self.nt*self.nf, self.p, self.p))
        else:
            self.nt = 1
            self.nf, self.p, _ = np.shape(wper)
            self.wper = wper
        self.instr = instr
        self.sgwb = sgwb
        self.inf = inf
        # Number of dimensions
        self.p = self.wper.shape[-1]
        # Number of frequency bins
        self.nf = len(freqs)
        # Number of time bins
        if wper.ndim == 4:
            self.nt = wper.shape[1]
            # Flatten the time and frequency dimensions
            self.wper_flat = np.reshape(self.wper, (self.nf*self.nt, self.p, self.p))
            # Number of DoF (repeat for each time bin)
            self.k_seg = np.tile(k_seg, self.nt)
        elif wper.ndim == 3:
            self.nt = 1
            self.wper_flat = wper
            # Number of DoF
            self.k_seg = k_seg
        else:
            print("Wrong number of spectrum dimensions !")
        # Inverse of periodogram matrix
        _, self.wper_det = utils.sym_matrix_inv(
            self.wper_flat, output_det=True)
        self.wper_logdet = np.log(self.wper_det)
        # # Compute the inverse and determinant of the periodogram
        # _, ws, _ = np.linalg.svd(self.wper_flat)
        # self.wper_logdet = np.sum(np.log(ws), axis=1)

        # Number of noise parameters to fit
        if self.instr is None:
            self.instr_ndim = 0
        elif not isinstance(self.instr, list):
            # Number of noise parameters
            self.instr_ndim = self.instr.ndim
        else:
            self.instr_ndim = sum([ins.ndim for ins in self.instr])
            # Localise the individual noise parameters in the full noise parameter vector
            self.ib = [0]
            self.ie = [self.instr[0].ndim]
            for i in range(1, len(self.instr)):
                self.ib.append(self.ie[i-1])
                self.ie.append(self.ie[i-1] + self.instr[i].ndim)
        # If there is at least one signal to fit
        if self.sgwb is not None:
            # If there is only one SGWB component
            if not isinstance(self.sgwb, list):
                self.sgwb_ndim = self.sgwb.ndim
            else:
                self.sgwb_ndim = sum([gw.ndim for gw in self.sgwb])
                # # Localise the individual SGWB parameters in the full signal parameter vector
                self.sib = [0]
                self.sie = [self.sgwb[0].ndim]
                for i in range(1, len(self.sgwb)):
                    self.sib.append(self.sie[i-1])
                    self.sie.append(self.sie[i-1] + self.sgwb[i].ndim)
        # If there is no signal to fit
        else:
            self.sgwb_ndim = 0

        # Total number of dimensions
        self.ndim = self.instr_ndim + self.sgwb_ndim

        # Data-dependent constant
        self.const = 0.0
        # self.const = np.sum((self.k_seg - self.p) * self.wper_logdet.real)
        # self.const += np.sum((self.k_seg - self.p) * self.p * np.log(self.k_seg))
        # self.const -= p * (p-1) / 2 * np.log(np.pi)
        # self.const -= np.sum(sum([special.gamma(self.k_seg-j+1) for j in range(1, p+1)]))

    def compute_signal_covariance(self, theta_gw):
        """
        Calculate the SGWB covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of SGWB parameters

        Returns
        -------
        cov_xyz_gw : ndarray
            TDI SGWB covariance of size nf x 3 x 3

        """
        # Hypothesis H1
        if self.sgwb is not None:
            # If there is only one GW signal model
            if not isinstance(self.sgwb, list):
                cov_xyz_gw = self.sgwb.compute_covariances(theta_gw)
            # If there are several GW signal models
            else:
                cov_xyz_gw = sum([self.sgwb[i].compute_covariances(
                    theta_gw[self.sib[i]:self.sie[i]])
                                 for i in range(len(self.sgwb))])
        # Hypothesis H0
        else:
            cov_xyz_gw = 0.0

        return cov_xyz_gw

    def compute_noise_covariance(self, theta_n):
        """
        Calculate the noise covariance of TDI XYZ

        Parameters
        ----------
        theta_n : ndarray
            vector of noise parameters

        Returns
        -------
        cov_xyz_n : ndarray
            TDI noise covariance of size nf x 3 x 3

        """
        if self.instr is None:
            cov_xyz_n = 0.0
        # If there is only one noise model
        elif not isinstance(self.instr, list):
            cov_xyz_n = self.instr.compute_covariances(theta_n)
        # If there are several noise models
        else:
            cov_xyz_n = sum([self.instr[i].compute_covariances(theta_n[self.ib[i]:self.ie[i]])
                             for i in range(len(self.instr))])

        return cov_xyz_n

    def compute_covariance(self, theta, flatten=False):
        """
        Calculate the covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.
        flatten : ndarray
            if True, merges the frequency and time dimensions.
            Default is False.

        Returns
        -------
        cov_xyz : ndarray
            frequency (and time) dependent covariance of size nf x 3 x 3
            or nf x nt x 3 x 3
        """
        
        # Signal-only
        if self.instr is None:
            cov_xyz_n = 0.0
            # SGWB contribution to covariance
            cov_xyz_gw = self.compute_signal_covariance(theta)
        else:
            # Hypothesis H1
            if self.sgwb is not None:
                # Noise parameters
                theta_n = theta[0:self.instr_ndim]
                # SGWB parameters
                theta_gw = theta[self.instr_ndim:]
                # SGWB contribution to covariance
                cov_xyz_gw = self.compute_signal_covariance(theta_gw)
                # Noise contribution to TDI covariance
                cov_xyz_n = self.compute_noise_covariance(theta_n)
            # Hypothesis H0
            else:
                cov_xyz_gw = 0.0
                # Noise contribution to TDI covariance
                cov_xyz_n = self.compute_noise_covariance(theta)

        if flatten & (self.nt > 1):
            # Concatenate frequency and time dimension in one row
            return np.reshape(cov_xyz_n + cov_xyz_gw, (self.nf*self.nt, self.p, self.p))

        return cov_xyz_n + cov_xyz_gw

    def evaluate(self, theta, real=False, svd=False):
        """
        Calculate the log-likelihood.

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        ll : float
            log-likelihood value at x, computed from finds frequencies and possibly times.
        """

        # Compute TDI covariance
        cov_xyz = self.compute_covariance(theta, flatten=True)
        # If real Wishart distribution, adjust
        if real:
            # Transform to real
            cov_xyz = (cov_xyz + np.conj(cov_xyz)) / 2.0
            nu = self.k_seg / 2
        else:
            nu = self.k_seg
        if svd:
            # Compute the inverse and determinant of the covariance
            u, s, vh = np.linalg.svd(cov_xyz, hermitian=True)
            cov_xyz_inv = utils.multiple_dot(np.swapaxes(vh, 1, 2).conj(),
                                             (s**-1)[:, :, np.newaxis] * np.swapaxes(u, 1, 2).conj())
            log_det = np.sum(np.log(s), axis=1)
        else:
            # Compute the inverse and determinant of the covariance
            cov_xyz_inv, det = utils.sym_matrix_inv(cov_xyz, output_det=True)
            log_det = np.log(det)
        # Compute C^{-1} P for all frequencies (and times)
        epsilon = utils.multiple_dot(cov_xyz_inv, self.wper)
        # Compute parameter-dependent parts of log-likelihood for all frequencies
        log_likelihood = - np.sum(nu * (np.trace(epsilon, axis1=1, axis2=2) + log_det)).real
        # Prevent NaNs
        if np.isnan(log_likelihood):
            log_likelihood = - self.inf
            warnings.warn("Loglikelihood NaN value was replaced by -inf")

        return log_likelihood + self.const


class TDICovarianceLikelihoodDynamic:

    def __init__(self, freqs, wper, k_seg, cov_models=None, inf=1e14, ftol=1e-2,
                 hypertriangle=False, expmax=200, interpolation_kind='Akima', 
                 use_edges=True, whiten=None):
        """
        Gaussian likelihood model the full XYZ Welch spectrum matrix.

        Parameters
        ----------
        freqs : ndarray
            Vector of frequencies
        wper : ndarray
            Welch periodogram matrix at frequencies`freqs`, size nf x 3 x 3
        k_seg : int
            number of segments used for the Welch averaging
        inf : float or np.inf
            if the likelihood diverge, it will be set equal to - inf
        cov_models : dictionary
            A dictionary with the information about the models contributing to the total covariance. This means
            that both noise and signal contributions enter here. The keys of the dictionary are used as the 
            names of each model.
            
            Each entry can contain ndarrays with transfer functions or instrument instance. Those will be used 
            to assess if each particular entry is a shape-agnostic spline model or an analytic one. Keys can 
            also contain analytic models (instrument or signal objects).
            
            Example: cov_models = {'model1': ndarray (nf x 3 x 6), 
                                   'model2': ndarray (nf x 3 x 6), 
                                   'model3': instr_1, 
                                   'model4': instr_2, 
                                   ...
                                   }
              
        signal_models : ndarray or lsit of ndarray objects
            Same as above, but for the signal
        hypertriangle : bool
            if True, the likelihood will operate a transformation on the knot parameters
            such that the transformed parameters are orderered knot locations.
        interpolation_kind: string
            The kind of interpolation to be passed to the interp1d function.
        expmax : float
            maximum value allowed in the exponential function. If this is reached,
            the log-likelihood will return -infinity.
        whiten : dictionary
            A dictionary containing a numerical spectrum for whitening the data. 
        use_edges : bool
            Flag to use a double model for the spline case. The double model includes 
            a model for the tfree knots at the center of the spectrum, plus the non-dynamical
            model of the fixed "edges" amplitudes at the minimum and maximum frequency respectively. 

        """

        self.freqs = freqs
        self.logfr = np.log(freqs)
        self.wper = wper
        self.inf = inf
        self.ftol = ftol
        self.hypertriangle = hypertriangle
        self.expmax = expmax  # Maximum value allowed in the exponential function
        self.kind = interpolation_kind  # Interpolation kind
        self.use_edges = use_edges
        # handle the interpolation kind
        if self.kind.lower() == "akima":
            self.interp_func = lambda x, y : interpolate.Akima1DInterpolator(x, y, axis=-1)(self.logfr)
            
        elif self.kind.lower() in ['linear', 'zero', 'slinear', 'quadratic', 'cubic', 'previous']:
            self.interp_func = lambda x, y : interpolate.interp1d(x, y,
                                                        kind=self.kind, axis=-1, copy=True,
                                                        bounds_error=False,
                                                        fill_value="extrapolate",
                                                        assume_sorted=self.hypertriangle)(self.logfr)
            
        elif self.kind.lower() in ['pchip', 'pchip_interpolate']:
            self.interp_func = lambda x, y : interpolate.pchip_interpolate(x, y, self.logfr)
            
        else:
            raise TypeError("### Error: The likelihood can use only the Akima or the interp1d functions.")
        
        self.noise_models = [] # initialize the number of noise models (splines plus analytic)
        self.signal_models = []
        self._cov_tot = None # Initialize the total covariance matrix (get it for each eval)
        # Loop over the number of transfer functions (or noise components)
        if cov_models is None: raise TypeError("### Error: The noise_models can not be None. Please provide a set of noise models.")
        self.cov_models = cov_models
        self.whiten = whiten
        self.cov_contr = dict()
        self.num_models = len(cov_models.keys())
        # Mark the index where each model parameters start
        self.minds = dict()
        total_param_groups = 0
        for mdl in self.cov_models:
            if isinstance(self.cov_models[mdl], np.ndarray): 
                self.minds[mdl] = [total_param_groups, total_param_groups+2]
                total_param_groups += 2  if self.use_edges else 1 # Can have two groups of parameters (it's a double model: free knots and edges)
            else:
                self.minds[mdl] = [total_param_groups, total_param_groups+1]
                total_param_groups += 1  # Has one group of parameters (single model)

        # Number of segments
        self.k_seg = k_seg
        # Number of dimensions
        self.p = self.wper.shape[2]

        # Inverse of periodogram matrix
        self.wper_inv, self.wper_det = utils.sym_matrix_inv(
            self.wper, output_det=True)

        # Data-dependent constant
        p = self.wper.shape[2]
        self.const = np.sum((self.k_seg - p) * np.log(np.linalg.det(self.wper)).real)
        self.const += np.sum((self.k_seg - p) * p * np.log(self.k_seg))        
    
    def compute_spline_psd(self, x, groups):
        """Get the spline model for the a given PSD series, given some knots

        Parameters
        ----------
        x, groups : ndarray
            PSD parameters and groups of the dynamical models

        Returns
        -------
        psd, failed : interpolate.interp1d evaluated, list of indices that failed
        """

        x_knots = x[0][:, 0]
        y_knots = x[0][:, 1]
        group_free_knots = groups[0]
        
        # Consider two models. One handling the internal knots, and one for the edges
        if self.use_edges:
            y_knots_edges = x[1] # Get the edges info
            group_edges = groups[1]                    

        num_groups = int(group_free_knots.max() + 1)
        log_psd_model = np.empty((num_groups, len(self.freqs)))
        log_psd_model[:] = np.nan
        failed = {}
        # Loop over the temperatures vs walkers
        for i in range(num_groups):
            inds1 = np.where(group_free_knots == i)
            x_knots_i = x_knots[inds1]
            y_knots_i = y_knots[inds1]

            if self.use_edges:
                inds2 = np.where(group_edges == i)
                y_knots_edges_i = np.squeeze(y_knots_edges[inds2])

            # Remove zeros ### Think about this again!
            x_knots_i = x_knots_i[x_knots_i != 0.]
            y_knots_i = y_knots_i[y_knots_i != 0.]

            if self.hypertriangle:
                # Re-order the knot location parameters by hypertriangulation
                x_knots_i = utils.hypertriangulate(x_knots_i,
                                                    bounds=(self.logfr[0], self.logfr[-1]))
            
            if self.use_edges: # Add the min and max frequency, as well as their knot amplitude
                x_knots_i = np.array([self.logfr[0]] + list(x_knots_i) + [self.logfr[-1]])
                y_knots_i = np.array([y_knots_edges_i[0]] + list(y_knots_i) + [y_knots_edges_i[-1]])

            # Sort them
            sort_ids = np.argsort(x_knots_i)
            x_knots_i = x_knots_i[sort_ids]
            y_knots_i = y_knots_i[sort_ids]

            # Control for knots very close to each other
            if not np.any(np.absolute(np.diff(np.array(x_knots_i))) < self.ftol):
                
                # Change the data and reset the spline class
                log_psd_model[i] = self.interp_func(x_knots_i, y_knots_i)

                # To prevent overflow
                if np.any(log_psd_model[i] > self.expmax):
                    i_over = np.where((log_psd_model[i] > self.expmax) | (
                        np.isnan(log_psd_model[i])))
                    log_psd_model[i][i_over] = np.nan
                    failed[i] = i_over

        return np.exp(log_psd_model)
    
    def compute_covariance(self, x, groups):
        """
        Calculate the covariance of TDI XYZ

        Parameters
        ----------
        x : ndarray
            vector of noise parameters + SGWB parameters.
        groups: ndarray
            vector of groups for the dynamical models.
        Returns
        -------
        cov_xyz : ndarray
            frequency-dependent covariance of size nf x 3 x 3
        """
        niter = 0
        for mdl in self.cov_models:
            if isinstance(self.cov_models[mdl], np.ndarray): # This entry is assumed to be a tdi noise transfer function
                
                spline_psd = self.compute_spline_psd(x[self.minds[mdl][0]:self.minds[mdl][1]], 
                                                     groups[self.minds[mdl][0]:self.minds[mdl][1]])
                
                # If we have chosen to fit the "whitened" spectrum
                if self.whiten is not None and mdl in self.whiten:
                    spline_psd *= self.whiten[mdl]
                    
                self.cov_contr[mdl] = self.cov_models[mdl] * spline_psd[:, :, np.newaxis, np.newaxis]  # The model here is a "tdi_corr" matrix
            else:
                pvals = np.array(x[self.minds[mdl][0]:self.minds[mdl][1]]).squeeze()
                self.cov_contr[mdl] = self.cov_models[mdl]( pvals )   # The model here is an analytic function

            if niter == 0: # I do this in order to avoid initializing (I might have different walkers and temperatures, or even none)
                self._cov_tot = self.cov_contr[mdl].copy() # Add the contribution to the total cov matrix
            else:
                self._cov_tot += self.cov_contr[mdl] # Add the contribution to the total cov matrix
            niter += 1
            
        return self._cov_tot

    def evaluate(self, x, groups):
        """
        Calculate the log-likelihood.

        Parameters
        ----------
        x : ndarray
            vector of noise parameters + SGWB parameters.
        groups: ndarray
            vector of groups for the dynamical models.

        Returns
        -------
        ll : float
            log-likelihood value at x, computed from finds frequencies.
        """

        # Compute TDI covariance
        cov_xyz = self.compute_covariance(x, groups)
        # Initialize the likelihood (N_temps times N_walkers)
        log_likelihood = np.full(cov_xyz.shape[0], - self.inf)
        # Compute the inverse and determinant of the covariance
        for i in range(cov_xyz.shape[0]):
            # Compute the eigendecomposition of the covariance
            cov_xyz_inv, det = utils.sym_matrix_inv(
                cov_xyz[i], output_det=True)
            # Compute C^{-1} P
            epsilon = utils.multiple_dot(cov_xyz_inv, self.wper)
            # Compute parameter-dependent parts of log-likelihood for all frequencies
            log_likelihood[i] = - np.sum(self.k_seg * (
                np.trace(epsilon, axis1=1, axis2=2) + np.log(det))).real
            # Prevent NaNs
            if np.isnan(log_likelihood[i]):
                log_likelihood[i] = - self.inf
        return log_likelihood + self.const


class TDICovarianceFixedNoiseLikelihood:

    def __init__(self, freqs, wper, instr, sgwb, k_seg, inf=1e14):
        """
        Gaussian likelihood model the full XYZ Welch spectrum matrix,
        but with noise PSD model fixed.

        Parameters
        ----------
        freqs : ndarray
            Vector of frequencies
        wper : ndarray
            Welch periodogram matrix at frequencies`freqs`, size nf x 3 x 3
        instr : NoisePSD instance
            class to compute the instrumental PSD
        sgwb : SignalPSD instance
            class to compute the SGWB PSD
        k_seg : int
            number of segments used for the Welch averaging
        inf : float or np.inf
            if the likelihood diverge, it will be set equal to - inf

        """

        self.freqs = freqs
        self.wper = wper
        self.instr = instr
        self.sgwb = sgwb
        self.inf = inf

        # TDI correlation matrix
        self.tdi_corr = utils.multiple_dot(
            self.instr.tdi_tf, np.swapaxes(self.instr.tdi_tf, 1, 2).conj())

        # Number of segments
        self.k_seg = k_seg

        # Number of parameters to fit
        self.ndim = self.sgwb.ndim

        # Noise PSD at link level
        s_n = self.instr.compute_link_psd(self.freqs)
        # Compute noise contribution to TDI covariance
        self.cov_xyz_n = self.tdi_corr * s_n[:, np.newaxis, np.newaxis]

    def compute_signal_covariance(self, theta_gw):
        """
        Calculate the SGWB covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of SGWB parameters

        Returns
        -------
        cov_xyz_gw : ndarray
            TDI SGWB covariance of size nf x 3 x 3

        """
        # SGWB PSD at link level
        s_h = self.sgwb.compute_strain_psds(theta_gw)
        # SGWB contribution to covariance
        cov_xyz_gw = self.sgwb.g_mat * s_h[:, np.newaxis, np.newaxis]

        return cov_xyz_gw

    def compute_noise_covariance(self):
        """
        Calculate the noise covariance of TDI XYZ

        Parameters
        ----------
        theta_n : ndarray
            vector of noise parameters

        Returns
        -------
        cov_xyz_n : ndarray
            TDI noise covariance of size nf x 3 x 3

        """

        return self.cov_xyz_n

    def compute_covariance(self, theta):
        """
        Calculate the covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        cov_xyz : ndarray
            frequency-dependent covariance of size nf x 3 x 3
        """

        # SGWB parameters
        theta_gw = theta[:]
        # SGWB contribution to covariance
        cov_xyz_gw = self.compute_signal_covariance(theta_gw)

        return self.cov_xyz_n + cov_xyz_gw

    def evaluate(self, theta):
        """
        Calculate the log-likelihood.

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        ll : float
            log-likelihood value at x, computed from finds frequencies.
        """

        # Compute TDI covariance
        cov_xyz = self.compute_covariance(theta)
        # Compute the eigendecomposition of the covariance
        cov_xyz_inv, det = utils.sym_matrix_inv(cov_xyz, output_det=True)
        # Compute C^{-1} P
        epsilon = utils.multiple_dot(cov_xyz_inv, self.wper)
        # Compute parameter-dependent parts of log-likelihood for all frequencies
        log_likelihood = - \
            np.sum(self.k_seg *
                   (np.trace(epsilon, axis1=1, axis2=2) + np.log(det))).real
        # Prevent NaNs
        if np.isnan(log_likelihood):
            log_likelihood = - self.inf
            warnings.warn("Loglikelihood NaN value was replaced by -inf")

        return log_likelihood


class TDICovarianceLikelihoodDynamic_old:

    def __init__(self, freqs, wper, sgwb, tdi_tf, k_seg, inf=1e14, ftol=1e-2,
                 hypertriangle=False, interpolation_kind='cubic', expmax=200):
        """
        Gaussian likelihood model the full XYZ Welch spectrum matrix.

        Parameters
        ----------
        freqs : ndarray
            Vector of frequencies
        wper : ndarray
            Welch periodogram matrix at frequencies`freqs`, size nf x 3 x 3
        sgwb : SignalPSD instance
            class to compute the SGWB PSD
        tdi_tf : ndarray
            TDI transfer function, size nf x 3 x 6
        k_seg : int
            number of segments used for the Welch averaging
        inf : float or np.inf
            if the likelihood diverge, it will be set equal to - inf
        ftol : float 
            distance tolerance between knots.    
        hypertriangle : bool
            if True, the likelihood will operate a transformation on the knot parameters
            such that the transformed parameters are orderered knot locations.
        interpolation_kind: string
            The kind of interpolation to be passed to the interp1d function.
        expmax : float
            maximum value allowed in the exponential function. If this is reached,
            the log-likelihood will return -infinity.

        """

        self.freqs = freqs
        self.logfr = np.log(freqs)
        self.wper = wper
        self.hypertriangle = hypertriangle
        self.sgwb = sgwb
        self.inf = inf
        self.kind = interpolation_kind  # Interpolation kind
        self.expmax = expmax  # Maximum value allowed in the exponential function
        self.ftol = ftol
        self.tdi_corr = utils.multiple_dot(tdi_tf, np.swapaxes(
            tdi_tf, 1, 2).conj())  # TDI correlation matrix
        self.k_seg = k_seg  # Number of segments

    def compute_signal_covariance(self, theta_gw):
        """
        Calculate the SGWB covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of SGWB parameters

        Returns
        -------
        cov_xyz_gw : ndarray
            TDI SGWB covariance of size nf x 3 x 3

        """
        # Hypothesis H1
        if self.sgwb is not None:
            # SGWB PSD at link level
            s_h = self.sgwb.compute_strain_psds(theta_gw)
            # SGWB contribution to covariance
            cov_xyz_gw = self.sgwb.g_mat * s_h[:, np.newaxis, np.newaxis]
        # Hypothesis H0
        else:
            cov_xyz_gw = 0.0

        return cov_xyz_gw

    def compute_link_psd(self, x, groups):
        """Get the spline model for the noise PSD, given some knots

        Parameters
        ----------
        x, groups : ndarray
            PSD parameters

        Returns
        -------
        instr : interpolate.interp1d evaluated
        """

        # I will consider two models. One handling the internal knots, and one for the edges
        x1, x2 = x
        group1, group2 = groups
        knots = x1[:, 0]
        control_points = x1[:, 1]

        # Get the edges info
        control_points_edges = x2

        num_groups = int(group1.max() + 1)
        # log_psd_model = np.zeros((num_groups, len(self.freq)))
        log_psd_model = np.empty((num_groups, len(self.freqs)))
        log_psd_model[:] = np.nan
        failed = {}

        # Loop over the temperatures vs walkers
        for i in range(num_groups):
            inds1 = np.where(group1 == i)
            knots_i = knots[inds1]
            control_points_i = control_points[inds1]

            inds2 = np.where(group2 == i)
            control_points_edges_i = np.squeeze(control_points_edges[inds2])

            # Remove zeros ### Think about this again!
            knots_i = knots_i[knots_i != 0.]
            control_points_i = control_points_i[control_points_i != 0.]

            if self.hypertriangle:
                # Re-order the knot location parameters by hypertriangulation
                x_knots = utils.hypertriangulate(knots_i,
                                                 bounds=(self.logfr[0], self.logfr[-1]))
            else:
                x_knots = knots_i

            knots_list = np.array(
                [self.logfr[0]] + list(x_knots) + [self.logfr[-1]])
            control_pts = np.array(
                [control_points_edges_i[0]] + list(control_points_i) + [control_points_edges_i[-1]])

            # Control for knots very close to each other
            if not np.any(np.diff(np.array(knots_list)) < self.ftol):
                # Change the data and reset the spline class
                interp_model = interpolate.interp1d(knots_list, control_pts,
                                                    kind=self.kind, axis=-1, copy=True,
                                                    bounds_error=False,
                                                    fill_value="extrapolate",
                                                    assume_sorted=self.hypertriangle)
                log_psd_model[i] = interp_model(self.logfr)

                # To prevent overflow
                if np.any(log_psd_model[i] > self.expmax):
                    warnings.warn("Overflow!")
                    i_over = np.where((log_psd_model[i] > self.expmax) | (
                        np.isnan(log_psd_model[i])))
                    log_psd_model[i][i_over] = np.nan
                    failed[i] = i_over

        return np.exp(log_psd_model), failed

    def compute_noise_covariance(self, x, groups):
        """
        Calculate the noise covariance of TDI XYZ

        Parameters
        ----------
        theta_n : ndarray
            vector of noise parameters

        Returns
        -------
        cov_xyz_n : ndarray
            TDI noise covariance of size nf x 3 x 3

        """
        # Noise PSD at link level
        s_n, _ = self.compute_link_psd(x, groups)

        # Compute noise contribution to TDI covariance
        cov_xyz_n = self.tdi_corr * s_n[:, :, np.newaxis, np.newaxis]
        # sn_aet = self.tdi_coeff * noise_psd_model[:, :, np.newaxis]
        return cov_xyz_n

    def compute_covariance(self, x, groups):
        """
        Calculate the covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        cov_xyz : ndarray
            frequency-dependent covariance of size nf x 3 x 3
        """

        # Compute noise contribution to TDI covariance
        cov_xyz_n = self.compute_noise_covariance(x, groups)

        # Hypothesis H1
        if self.sgwb is not None:
            # SGWB contribution to covariance
            cov_xyz_gw = self.compute_signal_covariance(x, groups)
            return cov_xyz_n + cov_xyz_gw
        # Hypothesis H0
        else:
            return cov_xyz_n

    def evaluate(self, x, groups):
        """
        Calculate the log-likelihood.

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        ll : float
            log-likelihood value at x, computed from finds frequencies.
        """
        # Compute TDI covariance
        cov_xyz = self.compute_covariance(x, groups)
        # Initialize the likelihood (N_temps times N_walkers)
        log_likelihood = np.full(cov_xyz.shape[0], - self.inf)
        # Loop over the number of likelihoods computed
        for i in range(cov_xyz.shape[0]):
            # Compute the eigendecomposition of the covariance
            cov_xyz_inv, det = utils.sym_matrix_inv(
                cov_xyz[i], output_det=True)
            # Compute C^{-1} P
            epsilon = utils.multiple_dot(cov_xyz_inv, self.wper)
            # Compute parameter-dependent parts of log-likelihood for all frequencies
            log_likelihood[i] = - np.sum(self.k_seg * (
                np.trace(epsilon, axis1=1, axis2=2) + np.log(det))).real
            # Prevent NaNs
            if np.isnan(log_likelihood[i]):
                log_likelihood[i] = - self.inf
                warnings.warn("Loglikelihood NaN value was replaced by -inf")

        return log_likelihood


class GeneralTDICovarianceLikelihood:

    def __init__(self, freqs, per_y, tdi_tf, x_mat, k_seg,
                 gw_mat=None, gw_psd=None, ndim_gw=0, inf=1e14,
                 log_psd=True):
        """
        Gaussian likelihood model the full XYZ Welch spectrum matrix.

        Parameters
        ----------
        freqs : ndarray
            Vector of frequencies, size nf
        per_y : ndarray
            Periodogram matrix at frequencies`freqs`, size nf x 3 x 3
        tdi_tf :ndarray
            TDI transformation matrix, size nf x 3 x 6
        x_mat : ndarray
            Spline design matrix, size nf x q
        k_seg : int
            number of segments used for the Welch averaging
        gw_mat : ndarray
            GW correlation matrix in the TDI domain, size nf x 3 x 3
        gw_psd : callable
            SGWB power spectral density function (of frequency)
        inf : float or np.inf
            if the likelihood diverge, it will be set equal to - inf
        log_psd : bool
            if True, x_mat is the regression basis for the log-PSD.
            if False, it is directly the PSD.

        """

        self.freqs = freqs
        self.per_y = per_y
        self.tdi_tf = tdi_tf
        self.gw_mat = gw_mat
        self.gw_psd = gw_psd
        self.x_mat = x_mat
        self.inf = inf
        self.k_seg = k_seg
        self.log_psd = log_psd

        # Number of frequency bins
        self.nf = freqs.shape[0]
        # Number of TDI channels
        self.p = tdi_tf.shape[1]
        # Size of the regression vector for one channel
        self.q = x_mat.shape[1]
        # Dimension of the noise parameter space
        self.ndim_n = 2 * self.q
        # Dimension of the signal parameter space
        self.ndim_gw = ndim_gw
        # Dimension of the full parameter space
        self.ndim = self.ndim_n + self.ndim_gw

        # Perform the TDI deconvolution
        self.u_mat, self.s_mat, _ = np.linalg.svd(self.tdi_tf)
        # Transformation matrix of the data
        self.s_mat_diag = np.array([np.diag(s) for s in self.s_mat])
        self.s_mat_diag_inv = np.array([np.diag(1/s) for s in self.s_mat])
        self.transform = utils.multiple_dot(
            self.s_mat_diag_inv, np.swapaxes(self.u_mat.conj(), 1, 2))
        # Inverse transformation
        self.transform_inv = utils.multiple_dot(self.u_mat, self.s_mat_diag)
        # Apply the transformation to the periodogram
        self.per = utils.transform_covariance(self.transform, self.per_y)
        if self.gw_mat is not None:
            # Apply the transformation to the GW correlations
            self.gw_mat_z = utils.transform_covariance(
                self.transform, self.gw_mat)

    def beta_to_diag(self, theta_n):
        """
        Extract the eigenvalues of the covariance matrix from the regression
        parameters.

        Parameters
        ----------
        theta_n : ndarray
            noise parameters, size 2q

        """

        n_indep = int(theta_n.size/self.q)

        if n_indep == self.p:
            b_list = [theta_n[self.q * i:self.q *
                              (i+1)] for i in range(self.p)]

        elif n_indep == 2:
            b_list = [theta_n[0:self.q], theta_n[0:self.q], theta_n[self.q:]]

        # Create the diagonal with entries X beta^{i}, shape n x p
        diag = np.asarray([np.dot(self.x_mat, b) for b in b_list]).T

        return diag

    def compute_strain_psds(self, theta_gw, freqs=None):
        """
        Compute SGWB strain PSD (without LISA nor TDI response)

        Parameters
        ----------
        theta_gw : ndarray
            SGWB parameters (log Omega, n)
        freqs : ndarray
            Frequency array, if different from self.freq

        Returns
        -------
        link_psd : ndarray
            SGWB PSD, size nf

        """

        if freqs is None:
            freqs = self.freqs

        # Compute PSD
        return self.gw_psd(theta_gw, freqs=freqs)

    def compute_signal_covariance(self, theta_gw, transformed=True):
        """
        Calculate the SGWB covariance of data (transformed data or TDI XYZ)

        Parameters
        ----------
        theta : ndarray
            vector of SGWB parameters
        transformed : bool
            if True, compute the signal in the transformed data space 
            (i.e., not TDI)

        Returns
        -------
        cov_xyz_gw : ndarray
            SGWB covariance of size nf x 3 x 3

        """
        s_h = self.compute_strain_psds(theta_gw)

        if transformed:
            return self.gw_mat_z * s_h[:, np.newaxis, np.newaxis]
        return self.gw_mat * s_h[:, np.newaxis, np.newaxis]

    def compute_noise_covariance(self, theta_n, transformed=False):
        """
        Calculate the noise covariance of TDI XYZ

        Parameters
        ----------
        theta_n : ndarray
            vector of noise parameters

        Returns
        -------
        cov_xyz_n : ndarray
            TDI noise covariance of size nf x 3 x 3

        """

        # Create the diagonal with entries X beta^{i}, shape n x p
        diag = self.beta_to_diag(theta_n)
        sigma_n = np.zeros((self.nf, self.p, self.p), dtype=complex)

        for i in range(diag.shape[1]):
            # We model log(PSD)
            if self.log_psd:
                sigma_n[:, i, i] = np.exp(diag[:, i])
            else:
                sigma_n[:, i, i] = diag[:, i]

        if transformed:
            return sigma_n
        return utils.transform_covariance(self.transform_inv, sigma_n)

    def compute_covariance(self, theta, transformed=True):
        """
        Computes the covariance of z.

        Parameters
        ----------
        theta : ndarray
            vector of parameters (noise + signal)
        transformed_space : bool
            if True, returns the covariance of the transformed data
            Otherwise, returns the covariance in the TDI domain

        Returns
        -------
        sigma_z
            data covariance including noise and signal, size nf x p x p
        """

        # Compute noise covariance
        cov = self.compute_noise_covariance(
            theta[0:self.ndim_n], transformed=True)

        # Compute the SGWB covariance if necessary
        if self.gw_psd is not None:
            cov_gw = self.compute_signal_covariance(
                theta[self.ndim_n:], transformed=True)
            cov = cov + cov_gw

        # Transformed data space
        if transformed:
            return cov
        # Retransform in TDI domain only if necessary
        return utils.transform_covariance(self.transform_inv, cov)

    def evaluate(self, theta):
        """
        Calculate the log-likelihood.

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        ll : float
            log-likelihood value at x, computed from finds frequencies.
        """

        # Compute TDI covariance
        cov_xyz = self.compute_covariance(theta, transformed=True)
        # Compute the eigendecomposition of the covariance
        cov_xyz_inv, det = utils.sym_matrix_inv(cov_xyz, output_det=True)
        # Compute C^{-1} P
        epsilon = utils.multiple_dot(cov_xyz_inv, self.per)
        # Compute parameter-dependent parts of log-likelihood for all frequencies
        log_likelihood = - \
            np.sum(self.k_seg *
                   (np.trace(epsilon, axis1=1, axis2=2) + np.log(det))).real
        # Prevent NaNs
        if np.isnan(log_likelihood):
            log_likelihood = - self.inf
            warnings.warn("Loglikelihood NaN value was replaced by -inf")

        return log_likelihood

    
class TwoNoiseTDICovarianceLikelihood:

    def __init__(self, freqs, per_y, oms_tf, tm_tf, x_mat, k_seg,
                 gw_mat=None, gw_psd=None, ndim_gw=0, inf=1e14,
                fixed_knots=True):
        """
        Gaussian likelihood model the full XYZ Welch spectrum matrix.

        Parameters
        ----------
        freqs : ndarray
            Vector of frequencies, size nf
        per_y : ndarray
            Periodogram matrix at frequencies`freqs`, size nf x 3 x 3
        oms_tf :ndarray
            OMS noise to TDI transformation matrix, size nf x 3 x 6
        tm_tf :ndarray
            TM noise to TDI transformation matrix, size nf x 3 x 6
        x_mat : ndarray
            Spline design matrix, size nf x q
        k_seg : int
            number of segments used for the Welch averaging
        gw_mat : ndarray
            GW correlation matrix in the TDI domain, size nf x 3 x 3
        gw_psd : callable
            SGWB power spectral density function (of frequency)
        inf : float or np.inf
            if the likelihood diverge, it will be set equal to - inf

        """

        self.freqs = freqs
        self.logfreq = np.log(freqs)
        self.per = per_y
        self.tdi_tf = {"OMS": oms_tf, 
                       "TM": tm_tf}
        self.keys = ["OMS", "TM"]
        self.gw_mat = gw_mat
        self.gw_psd = gw_psd
        self.x_mat = x_mat
        self.inf = inf
        self.k_seg = k_seg
        self.fixed_knots = fixed_knots

        # Number of frequency bins
        self.nf = freqs.shape[0]
        # Number of TDI channels
        self.p = oms_tf.shape[1]
        # Number of coefficients to fit
        self.q = x_mat.shape[1]
        # Dimension of the noise parameter space
        if fixed_knots:
            self.ndim_n = 2 * self.q
        else:
            self.ndim_n = 2 * (2*self.q - 2)
        # Dimension of the signal parameter space
        self.ndim_gw = ndim_gw
        # Dimension of the full parameter space
        self.ndim = self.ndim_n + self.ndim_gw

        # Correlation matrix for OMS noise
        self.corr = {key: utils.multiple_dot(
            self.tdi_tf[key], np.swapaxes(self.tdi_tf[key].conj(), 1, 2))
                     for key in self.keys}
        
    def compute_single_link_noise_psds(self, theta_n):
        """
        Extract the PSDs of the single-link measurements 
        from the regression parameters.

        Parameters
        ----------
        theta_n : ndarray
            noise parameters, size 2q if knots are fixed.
            Otherwise, it should be ordered in the folliwng way:
            coeffs_1, x_knots_1, coeffs_2, x_knots_2

        """

        # Two parameter vectors if fixed knots
        # if self.fixed_knots:
        b_list = {"OMS": theta_n[0:self.q],
                  "TM": theta_n[self.q:]}
        # # If knots are not fixed, recompute the basis
        # else:
        #     b_list = {"OMS": theta_n[0:self.q],
        #               "TM": theta_n[2*self.q-2, 3*self.q-2]}  

        # Create the diagonal with entries X beta^{i}, shape n x p
        psds = {key: np.exp(np.dot(self.x_mat, b_list[key])) 
                for key in self.keys}

        return psds
    
    def compute_noise_covariance(self, theta_n):
        """
        Calculate the noise covariance of TDI XYZ

        Parameters
        ----------
        theta_n : ndarray
            vector of noise parameters

        Returns
        -------
        cov_xyz_n : ndarray
            TDI noise covariance of size nf x 3 x 3

        """

        # Create the diagonal with entries X beta^{i}, shape n x p
        s_n = self.compute_single_link_noise_psds(theta_n)
        sigma_n = [self.corr[key] * s_n[key][:, np.newaxis, np.newaxis] 
                   for key in self.keys]
        
        return sum(sigma_n)

    def compute_covariance(self, theta):
        """
        Calculate the full covariance of TDI XYZ

        Parameters
        ----------
        theta : ndarray
            vector of parameters (noise + signal)

        Returns
        -------
        sigma
            data covariance including noise and signal, size nf x p x p
        """

        # Compute noise covariance
        cov = self.compute_noise_covariance(theta[0:self.ndim_n])

        # Compute the SGWB covariance if necessary
        if self.gw_psd is not None:
            cov_gw = self.compute_signal_covariance(theta[self.ndim_n:])
            cov = cov + cov_gw
            
        return cov
    
    def compute_signal_covariance(self, theta_gw):
        """
        Calculate the SGWB covariance of data (transformed data or TDI XYZ)

        Parameters
        ----------
        theta : ndarray
            vector of SGWB parameters

        Returns
        -------
        cov_xyz_gw : ndarray
            SGWB covariance of size nf x 3 x 3

        """
        s_h = self.gw_psd(theta_gw, freqs=self.freqs)

        return self.gw_mat * s_h[:, np.newaxis, np.newaxis]
    
    def evaluate(self, theta):
        """
        Calculate the log-likelihood.

        Parameters
        ----------
        theta : ndarray
            vector of noise parameters + SGWB parameters.

        Returns
        -------
        ll : float
            log-likelihood value at x, computed from finds frequencies.
        """

        # Compute TDI covariance
        cov_xyz = self.compute_covariance(theta)
        # Compute the eigendecomposition of the covariance
        cov_xyz_inv, det = utils.sym_matrix_inv(cov_xyz, output_det=True)
        # Compute C^{-1} P
        epsilon = utils.multiple_dot(cov_xyz_inv, self.per)
        # Compute parameter-dependent parts of log-likelihood for all frequencies
        log_likelihood = - \
            np.sum(self.k_seg *
                   (np.trace(epsilon, axis1=1, axis2=2) + np.log(det))).real
        # Prevent NaNs
        if np.isnan(log_likelihood):
            log_likelihood = - self.inf
            warnings.warn("Loglikelihood NaN value was replaced by -inf")

        return log_likelihood
    
    def compute_design_matrix(self, x_knots, freq=None, kind="cubic"):
        """
        Computation of the spline design matrix.

        Parameters
        ----------
        x_knots : ndarray
            parameters for interior knots locations (log-frequencies).
        freq : ndarray or None
            frequencies where to compute the design matrix.
            if None, use the frequencies provided when 
            instantiating the class.

        Returns
        -------
        ndarray
            design matrix A such that the PSD can be written A.dot(coeffs)
        """

        # Add boundaries of the domain to the interior knots
        logf_knots = np.asarray([self.logfreq[0]] + list(x_knots) + [self.logfreq[-1]])
        # Change the data and reset the spline class
        basis_func = interpolate.interp1d(logf_knots, np.eye(logf_knots.size),
                                          kind=kind, 
                                          axis=-1, 
                                          copy=True,
                                          bounds_error=False,
                                          fill_value="extrapolate",
                                          assume_sorted=True)
        
        if freq is None:
            return basis_func(self.logfreq).T
        else:
            return basis_func(np.log(freq)).T