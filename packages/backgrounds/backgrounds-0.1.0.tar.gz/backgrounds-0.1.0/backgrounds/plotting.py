# -*- coding: utf-8 -*-
# Author: Quentin Baghi 2021 <quentin.baghi@protonmail.com>
import matplotlib as mpl
import numpy as np
from matplotlib import pyplot as plt
#from pyfftw.interfaces.numpy_fft import fft, ifft
from numpy.fft import fft, ifft
import matplotlib.colors as mc
import colorsys


def plotconfig(lbsize=17, lgsize=14, autolayout=True, figsize=[8, 6],
               ticklabelsize=16, fsize=15, fontfamily='STIXGeneral',
               tdir='in', major=10, minor=7, lwidth=2, lhandle=2.0,
               usetex=False, rcfonts=False, ticks_font_family='serif'):

 
    ticks_font = mpl.font_manager.FontProperties(family=ticks_font_family,
                                                 style='normal',
                                                 weight='normal',
                                                 stretch='normal',
                                                 size=lbsize)

    if fontfamily == 'STIXGeneral':
        mpl.rcParams['mathtext.fontset'] = 'stix'


    mpl.rcParams['text.usetex'] = usetex
    mpl.rcParams['pgf.rcfonts'] = usetex

    mpl.rcParams['font.family'] = fontfamily
    mpl.rcParams['figure.figsize'] = figsize[0], figsize[1]
    mpl.rcParams['figure.autolayout'] = autolayout
    mpl.rcParams['xtick.labelsize'] = ticklabelsize
    mpl.rcParams['ytick.labelsize'] = ticklabelsize
    plt.rcParams['font.size'] = fsize
    plt.rcParams['axes.linewidth'] = lwidth

    mpl.rcParams['axes.titlesize'] = lbsize
    mpl.rcParams['axes.labelsize'] = lbsize

    plt.rcParams['xtick.major.size'] = major
    plt.rcParams['xtick.minor.size'] = minor

    plt.rcParams['ytick.major.size'] = major
    plt.rcParams['ytick.minor.size'] = minor

    plt.rcParams['xtick.direction'] = tdir
    plt.rcParams['ytick.direction'] = tdir

    plt.rcParams['xtick.major.width'] = lwidth
    plt.rcParams['ytick.major.width'] = lwidth

    plt.rcParams['xtick.major.top'] = True
    plt.rcParams['xtick.minor.top'] = True
    plt.rcParams['ytick.major.right'] = True
    plt.rcParams['ytick.minor.right'] = True
    plt.rcParams['xtick.major.bottom'] = True
    plt.rcParams['xtick.minor.bottom'] = True
    plt.rcParams['ytick.major.left'] = True
    plt.rcParams['ytick.minor.left'] = True
    plt.rcParams['xtick.top'] = True    # draw ticks on the left side
    plt.rcParams['ytick.right'] = True   # draw ticks on the right side


def plotconfig_latex(fontsize=11.0, figsize=None, labelsize=17, ticklabelsize=16,
                     tickmajorsize=8, tickminorsize=6, tickminorwidth=1, tickmajorwidth=2):
    """Load matplotlib configuration for paper plots in latex.

    Parameters
    ----------
    fontsize : float, optional
        _description_, by default 11.0
    figsize : list, optional
        _description_, by default None
    labelsize : int, optional
        _description_, by default 17
    ticklabelsize : int, optional
        _description_, by default 16
    tickmajorsize : int, optional
        _description_, by default 10
    tickminorsize : int, optional
        _description_, by default 7
    """

    if figsize is None:
        figsize = [4.9, 3.5]

    mpl.rcParams["figure.figsize"] = figsize[0], figsize[1]
    mpl.rcParams["font.size"] = fontsize
    mpl.rcParams["font.family"] = "serif"
    # mpl.rcParams["font.serif"] = "Palatino"
    mpl.rcParams["axes.titlesize"] = "medium"
    mpl.rcParams["figure.titlesize"] = "medium"
    mpl.rcParams["text.usetex"] = True

    # Axes label sizes (x and y)
    mpl.rcParams['axes.labelsize'] = labelsize
    mpl.rcParams['axes.titlesize'] = labelsize
    # Axes ticks label sizes
    mpl.rcParams['xtick.labelsize'] = ticklabelsize
    mpl.rcParams['ytick.labelsize'] = ticklabelsize
    # Axes ticks sizes
    mpl.rcParams['xtick.major.size'] = tickmajorsize
    mpl.rcParams['xtick.minor.size'] = tickminorsize
    mpl.rcParams['ytick.major.size'] = tickmajorsize
    mpl.rcParams['ytick.minor.size'] = tickminorsize
    # Axes ticks widths
    mpl.rcParams['axes.linewidth'] = tickmajorwidth
    mpl.rcParams['xtick.major.width'] = tickmajorwidth
    mpl.rcParams['ytick.major.width'] = tickmajorwidth
    mpl.rcParams['xtick.minor.width'] = tickminorwidth
    mpl.rcParams['ytick.minor.width'] = tickminorwidth

    mpl.rcParams['xtick.major.top'] = True
    mpl.rcParams['xtick.minor.top'] = True
    mpl.rcParams['ytick.major.right'] = True
    mpl.rcParams['ytick.minor.right'] = True
    mpl.rcParams['xtick.major.bottom'] = True
    mpl.rcParams['xtick.minor.bottom'] = True
    mpl.rcParams['ytick.major.left'] = True
    mpl.rcParams['ytick.minor.left'] = True
    mpl.rcParams['xtick.top'] = True    # draw ticks on the left side
    mpl.rcParams['ytick.right'] = True   # draw ticks on the right side

    mpl.rcParams['xtick.direction'] = 'in'
    mpl.rcParams['ytick.direction'] = 'in'


def set_size(width=426.79135, fraction=1):
    """Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float
            Document textwidth or columnwidth in pts
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy

    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    # Width of figure (in pts)
    fig_width_pt = width * fraction

    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    # https://disq.us/p/2940ij3
    golden_ratio = (5**.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio

    fig_dim = (round(fig_width_in), round(fig_height_in))

    return fig_dim


def compute_periodogram(x, wd=None, fs=1.0):

    if wd is None:
        wd = np.hanning(x.shape[0])
    else:
        if type(wd) == str:
            if wd == 'hanning':
                wd = np.hanning(x.shape[0])
            elif wd == 'blackman':
                wd = np.blackman(x.shape[0])
            else:
                raise NotImplementedError("Window not implemented.")
        elif type(wd) == np.ndarray:
            pass
        else:
            TypeError("Window should be a string or an array")

    x_fft = fft(x * wd)
    k2 = np.sum(wd**2)

    return np.abs(x_fft) * np.sqrt(2 / (k2 * fs))


def lighten_color(color, amount=0.5):
    """
    Lightens the given color by multiplying (1-luminosity) by the given amount.
    Input can be matplotlib color string, hex string, or RGB tuple.

    Examples:
    >> lighten_color('g', 0.3)
    >> lighten_color('#F034A3', 0.6)
    >> lighten_color((.3,.55,.1), 0.5)
    """

    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], 1 - amount * (1 - c[1]), c[2])


class SpectralAnalysis:

    def __init__(self, fs=1.0, freqs=None, units='',
                 xlabel=r"Frequency [Hz]",
                 ylabel=None):

        # Sampling frequency
        self.fs = fs
        # Vector of frequencies
        self.freqs = freqs
        # Dictionary of time series
        self.series = {}
        self.series_colors = {}
        self.series_linestyles = {}
        # Dictionary of one-sided PSDs
        self.psds = {}
        self.psds_colors = {}
        self.psds_linestyles = {}

        self.xlabel = xlabel
        if ylabel is None:
            self.ylabel = 'PSD [' + units + r'$\mathrm{Hz^{-1/2}}$]'
        else:
            self.ylabel = ylabel
        self.colors = ['k', 'tab:blue', 'brown', 'gray']

    def add_time_series(self, x, name, color=None, linestyle='solid'):

        self.series[name] = x
        self.series_colors[name] = color
        self.series_linestyles[name] = linestyle

    def add_psd(self, psd, name, color=None, linestyle='solid'):

        self.psds[name] = psd.real
        self.psds_colors[name] = color
        self.psds_linestyles[name] = linestyle

    def plot(self, series_names=None, psd_names=None, title=None,
             left=None, right=None, bottom=None, top=None, wd=None,
             periodogram_lw=1, psd_lw=2, savepath=None, dpi=150,
             show=False):

        fig1, ax1 = plt.subplots(nrows=1)
        key_list = list(self.series.keys())

        for j, key in enumerate(key_list):
            # Plot periodograms
            pj = compute_periodogram(
                self.series[key], wd=wd, fs=self.fs)
            freqs = np.fft.fftfreq(pj.shape[0]) * self.fs
            inds = np.where(freqs > 0)[0]
            ax1.plot(freqs[inds], pj[inds],
                     color=self.colors[j],
                     label=key,
                     linewidth=periodogram_lw,
                     linestyle='solid',
                     rasterized=False)

        if self.freqs is not None:
            freqs = self.freqs
        inds = np.where(freqs > 0)[0]
        key_list = list(self.psds.keys())

        for j, key in enumerate(key_list):
            # Plot theoretical PSD if any
            if key_list[j] in self.psds:
                # PSD color
                if self.psds_colors[key] is not None:
                    color = self.psds_colors[key]
                else:
                    color = lighten_color(self.colors[j], amount=0.5)
                ax1.plot(freqs[inds],
                         np.sqrt(self.psds[key][inds]),
                         color=color,
                         label=key,
                         linewidth=psd_lw,
                         linestyle=self.psds_linestyles[key],
                         rasterized=False)

        ax1.set_xscale('log')
        ax1.set_yscale('log')
        ax1.set_xlabel(self.xlabel, fontsize=16)
        ax1.set_ylabel(self.ylabel, fontsize=16)
        if left is None:
            ax1.set_xlim(left=freqs[1], right=self.fs/2)
        if (bottom is not None) | (top is not None):
            ax1.set_ylim(bottom=bottom, top=top)
        ax1.set_title(title)
        ax1.grid(which='both', axis='both', linestyle='dotted', linewidth=1)
        ax1.minorticks_on()
        ax1.grid(color='gray', linestyle='dotted')
        plt.legend()
        if savepath is not None:
            plt.savefig(savepath, dpi=dpi)
        if show:
            plt.show()
        return fig1, ax1


def plot_single_link_posteriors(noise_classes, chaint, sn_true, titles=None,
                                ylabels=None, ylabels_errors=None,
                                ndraws = 500, psd_prior_up=None, psd_prior_low=None):
    # Frequencies
    finds = noise_classes[0].freq

    # Localise the individual noise parameters in the full parameter vector
    ib = [0] # Start from the beginning of the vector
    ie = [noise_classes[0].ndim] # Until the dimension of the first noise model
    for i, noise_comp in enumerate(noise_classes): # Then for each additional component
        # Start from where we were at the last iteration
        ib.append(ie[i-1]) 
        # Add the dimension of the new noise model
        ie.append(ie[i-1] + noise_comp.ndim)

    if titles is None:
        titles = ["OMS noise", "TM noise"]
    if ylabels is None:
        ylabels = [r"$\sqrt{S_{\mathrm{OMS}}}$ [$\mathrm{Hz^{-1/2}}$]",
                r"$\sqrt{S_{\mathrm{TM}}}$ [$\mathrm{Hz^{-1/2}}$]"]
    if ylabels_errors is None:
        ylabels_errors = [r"$\delta S_{\mathrm{OMS}} / S_{\mathrm{OMS}}$",
                          r"$\delta S_{\mathrm{TM}} / S_{\mathrm{TM}}$"]
    # Plot the OMS PSD estimate
    for j in range(2):
        fig, ax = plt.subplots(nrows=2, ncols=1, figsize=(8, 6),
                            gridspec_kw={'height_ratios': [2, 1]})
        y_max = np.sqrt(np.max(np.abs(sn_true[:, j]))*10)
        y_min = np.sqrt(np.min(np.abs(sn_true[:, j]))/10)

        for i in range(ndraws):
            theta_n = chaint[i, ib[j]:ie[j]]
            ax[0].plot(finds, np.sqrt(np.abs(noise_classes[j].compute_link_psd(theta_n))),
                    alpha=0.6, color='tab:blue', linewidth=0.5)

            if i == 0:
                ax[0].plot(finds, np.sqrt(np.abs(noise_classes[j].compute_link_psd(theta_n))),
                        alpha=0.6, 
                        color='tab:blue',
                        linewidth=0.5,
                        label='Posterior')
        if (psd_prior_up is not None) & (psd_prior_low is not None):
            ax[0].fill_between(finds, 
                            y1=np.sqrt(psd_prior_up[j]), 
                            y2=np.sqrt(psd_prior_low[j]), 
                            alpha=0.4,
                            label="Prior",
                            color='gray')

        ax[0].plot(finds, np.sqrt(np.abs(sn_true[:, j])),
                label='True PSD', 
                color='tab:orange', linewidth=1, linestyle='dashed')

        ax[0].set_xscale('log')
        ax[0].set_yscale('log')
        ax[0].legend(loc='upper right', frameon=False, ncol=3)
        ax[0].set_ylabel(ylabels[j])
        ax[0].set_title(titles[j])
        ax[0].set_xlim([finds[0], finds[-1]])

        # ---------
        # Residuals
        # ---------
        ax[1].set_xlabel(r"Frequency [Hz]")
        ax[1].set_ylabel(ylabels_errors[j])
        ax[1].set_xlim([1e-4, finds[-1]])

        for i in range(ndraws):
            theta_n = chaint[i, j*noise_classes[j].ndim:(j+1)*noise_classes[j].ndim]
            sn_post = noise_classes[j].compute_link_psd(theta_n)
            err = (sn_post - sn_true[:, j]) / sn_true[:, j]
            ax[1].plot(finds, np.real(err),
                    linestyle='solid',
                    linewidth=0.5,
                    color='tab:blue')

        ax[1].set_xscale('log')
        plt.tight_layout()

    return fig, ax


def plot_predictive_posteriors(chaint, loglike_cls, logprior_cls, n_draws=300, cov_tdi_true=None, k_sig=2,
                               signal_split=False, signal_keys="GW"):
    """
    Plot predictive posteriors from parameter chains and likelihood model.
    
    """
    
    # For the priors
    # --------------
    
    # Prior samples
    betas_prior = np.array([logprior_cls.initialize_single_param() for i in n_draws])
    
    # NOISE PRIOR
    # Dimension of the noise model parameter space
    ndim_n = loglike_cls.ndim_instr
    # Compute prior mean deviation of noise in TDI domain
    log_cov_tdi_n_mean = np.mean(np.array([np.log(loglike_cls.compute_noise_covariance(theta_[:ndim_n])) 
                                                 for theta_ in betas_prior]), axis=0)
    # Compute prior standard deviation of noise in TDI domain
    log_cov_tdi_n_var = np.var(np.array([np.log(loglike_cls.compute_noise_covariance(theta_[:ndim_n])) 
                                         for theta_ in betas_prior]), axis=0)
    # Compute the prior mean and variance
    tdi_prior_psd_mean = {}
    tdi_prior_psd_var = {}
    
    tdi_prior_psd_mean["noise"] = np.exp(np.asarray([log_cov_tdi_n_mean[..., i, i] for i in range(3)])).T
    tdi_prior_psd_var["noise"] = np.asarray([log_cov_tdi_n_var[..., i, i] for i in range(3)]).T
    
    tdi_prior_psd_up = {}
    tdi_prior_psd_low = {}

    # Compute prior credible intervals
    tdi_prior_psd_up["noise"] = np.exp(np.log(tdi_prior_psd_mean["noise"]) + k_sig * np.sqrt(tdi_prior_psd_var["noise"]))
    tdi_prior_psd_low["noise"] = np.exp(np.log(tdi_prior_psd_mean["noise"]) - k_sig * np.sqrt(tdi_prior_psd_var["noise"]))
    
    
    # GW PRIOR
    if loglike_cls.sgwb is not None:
        # Compute prior mean deviation of noise in TDI domain
        log_cov_tdi_gw_mean = np.mean(np.array([np.log(loglike_cls.compute_signal_covariance(theta_[ndim_n:])) 
                                                     for theta_ in betas_prior]), axis=0)
        # Compute prior standard deviation of noise in TDI domain
        log_cov_tdi_gw_var = np.var(np.array([np.log(loglike_cls.compute_signal_covariance(theta_[ndim_n:])) 
                                             for theta_ in betas_prior]), axis=0)
        # Compute the signal prior mean and variance
        tdi_prior_psd_mean["GW"] = np.exp(np.asarray([log_cov_tdi_n_mean[..., i, i] for i in range(3)])).T
        tdi_prior_psd_var["GW"] = np.asarray([log_cov_tdi_n_var[..., i, i] for i in range(3)]).T
        
        tdi_prior_psd_up["GW"] = np.exp(np.log(tdi_prior_psd_mean["GW"]) + k_sig * np.sqrt(tdi_prior_psd_var["GW"]))
        tdi_prior_psd_low["GW"] = np.exp(np.log(tdi_prior_psd_mean["GW"]) - k_sig * np.sqrt(tdi_prior_psd_var["GW"]))
    
    if cov_tdi_true is not None:
        # True injected values
        tdi_psd_true = {}

        # True TDI PSD
        tdi_psd_true["noise"] = np.asarray([cov_tdi_true["noise"][..., i, i] for i in range(3)]).T

        # True SGWB TDI PSD
        tdi_psd_true["GW"] = np.asarray([cov_tdi_n_true["GW"][..., i, i] 
                                         for i in range(3)]).T
    

    