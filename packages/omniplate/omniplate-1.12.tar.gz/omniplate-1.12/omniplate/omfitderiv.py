"""Smooth and estimate time derivatives via Gaussian processes."""

import copy
import warnings

import gaussianprocessderivatives as gp
import matplotlib.pylab as plt
import numpy as np
from scipy.interpolate import interp1d

import omniplate.admin as admin
import omniplate.omgenutils as gu
import omniplate.omstats as omstats


def runfitderiv(
    self,
    t,
    d,
    fitvar,
    derivname,
    experiment,
    condition,
    strain,
    bd=False,
    cvfn="matern",
    empirical_errors=False,
    noruns=10,
    exitearly=True,
    noinits=100,
    nosamples=100,
    logs=False,
    figs=True,
    findareas=False,
    plotlocalmax=True,
    showpeakproperties=False,
    linalgmax=5,
    max_data_pts=None,
    **kwargs,
):
    """
    Run fitderiv to smooth and estimate time derivatives for a single data set.

    Parameters
    ----------
    t: array
        An array of times.
    d: array
        An array of measurements of the variable to be fit.
    fitvar: string
        The name of the variable to be fit.
    derivname: string
        The name of the first time derivative of the variable.
    experiment: string
        The name of the experiment of interest.
    condition: string
        The condition of interest.
    strain: string
        The strain of interest.
    ylabels: list of strings
        The labels for the y-axis
    bd: dictionary, optional
        The bounds on the hyperparameters for the Gaussian process.
        For example, bd= {1: [-2,0])} fixes the bounds on the
        hyperparameter controlling flexibility to be 1e-2 and 1e0.
        The default for a Matern covariance function
        is {0: (-5,5), 1: (-4,4), 2: (-5,2)},
        where the first element controls amplitude, the second controls
        flexibility, and the third determines the magnitude of the
        measurement error.
    cvfn: string, optional
        The covariance function used in the Gaussian process, either
        'matern' or 'sqexp' or 'nn'.
    empirical_errors: boolean, optional
        If True, measurement errors are empirically estimated from the
        variance across replicates at each time point and so vary with
        time.
        If False, the magnitude of the measurement error is fit from the
        data assuming that this magnitude is the same at all time points.
    noruns: integer, optional
        The number of attempts made for each fit. Each attempt is made
        with random initial estimates of the hyperparameters within their
        bounds.
    exitearly: boolean, optional
        If True, stop at the first successful fit.
        If False, use the best fit from all successful fits.
    noinits: integer, optional
        The number of random attempts to find a good initial condition
        before running the optimization.
    nosamples: integer, optional
        The number of samples used to calculate errors in statistics by
        bootstrapping.
    logs: boolean, optional
        If True, find the derivative of the log of the data and should be
        True to determine the specific growth rate when dtype= 'OD'.
    figs: boolean, optional
        If True, plot both the fits and inferred derivative.
    findareas: boolean, optional
        If True, find the area under the plot of gr vs OD and the area
        under the plot of OD vs time. Setting to True can make getstats
        slow.
    plotlocalmax: boolean, optional
        If True, mark the highest local maxima found, which is used to
        calculate statistics, on any plots.
    showpeakproperties: boolean, optional
        If True, show properties of any local peaks that have found by
        scipy's find_peaks. Additional properties can be specified as
        kwargs and are passed to find_peaks.
    linalgmax: int, optional
        The number of linear algebra errors to tolerate.
    max_data_pts: integer, optional
        If set, sufficiently large data sets with multiple replicates will
        be subsampled at each time point, randomly picking a smaller
        number of replicates, to reduce the number of data points and so
        run times.
    """
    print(f"Fitting {fitvar} for {experiment}: {strain} in {condition}")
    # define statnames
    statnames = [
        f"min_{fitvar}",
        f"max_{fitvar}",
        f"range_{fitvar}",
        f"max_{derivname}",
        f"time_of_max_{derivname}",
    ]
    if derivname == "gr":
        # special names when estimating specific growth rate
        statnames += ["doubling_time", "lag_time"]
    else:
        statnames += [
            f"doubling_time_from_{derivname}",
            f"lag_time_from_{derivname}",
        ]
    # call fitderiv
    f = fitderiv(
        t,
        d,
        cvfn=cvfn,
        logs=logs,
        noruns=noruns,
        noinits=noinits,
        exitearly=exitearly,
        bd=bd,
        empirical_errors=empirical_errors,
        linalgmax=linalgmax,
        max_data_pts=max_data_pts,
    )
    if f.success:
        if figs:
            plt.figure()
            plt.subplot(2, 1, 1)
            f.plotfit(
                "f",
                ylabel=fitvar,
                figtitle=f"{experiment}: {strain} in {condition}",
            )
            axgr = plt.subplot(2, 1, 2)
            f.plotfit("df", ylabel=derivname)
            plt.tight_layout()
        else:
            axgr = None
        # find summary statistics
        (
            df_for_s,
            dict_for_sc,
            warning,
        ) = omstats.findsummarystats(
            fitvar,
            derivname,
            statnames,
            nosamples,
            f,
            t,
            experiment,
            condition,
            strain,
            findareas,
            figs,
            plotlocalmax,
            axgr,
            showpeakproperties,
            **kwargs,
        )
        # store GP parameters
        dict_for_sc[f"logmaxlikehood_for_{derivname}"] = f.logmaxlike
        dict_for_sc["gp_for_" + derivname] = cvfn
        for j, val in enumerate(f.lth):
            dict_for_sc[f"log_hyperparameter_{j}_for_{derivname}"] = val
        # add time series to s dataframe
        admin.add_to_s(self, derivname, df_for_s)
        # create or add summary stats to sc dataframe
        admin.add_dict_to_sc(self, dict_for_sc)
        if figs:
            plt.show(block=False)
        return f, warning
    else:
        return f, None


class fitderiv:
    """
    Smooth and estimate the time derivative of the data via Gaussian processes.

    After a successful optimisation, the following attributes are generated:

    t: array
        The times specified as input.
    d: array
        The data specified as input.
    f: array
        The mean of the Gaussian process with the optimal hyperparmeters
        at each time point.
    fvar: array
        The variance of the optimal Gaussian process at each time point.
    df: array
        The inferred first time-derivative.
    dfvar: array
        The inferred variance of the first time-derivative.
    ddf: array
        The inferred second time-derivative.
    ddfvar: array
        The inferred variance of the second time-derivative.

    Examples
    --------
    A typical work flow is:

    >>> from fitderiv import fitderiv
    >>> q= fitderiv(t, od, figs= True)
    >>> q.plotfit('df')

    or potentially

    >>> import matplotlib.pyplot as plt
    >>> plt.plot(q.t, q.d, 'r.', q.t, q.y, 'b')

    Reference
    ---------
    PS Swain, K Stevenson, A Leary, LF Montano-Gutierrez, IBN Clark, J Vogel,
    and T Pilizota.
    Inferring time derivatives including growth rates using Gaussian processes
    Nat Commun 7 (2016) 13766
    """

    def __init__(
        self,
        t,
        d,
        cvfn="matern",
        logs=True,
        noruns=5,
        noinits=100,
        exitearly=False,
        bd=False,
        empirical_errors=False,
        optmethod="L-BFGS-B",
        runtime_warn=False,
        linalgmax=3,
        max_data_pts=None,
        warn=False,
    ):
        """
        Smooth data and estimate time derivatives with a Gaussian process.

        Parameters
        ----------
        t: 1D array
            The time points.
        d: array
            The data corresponding to the time points with any replicates given
             as columns.
        cvfn: string
            The type of kernel function for the Gaussian process either 'sqexp'
            (squared exponential) or 'matern' (Matern with nu= 5/2) or 'nn'
            (neural network).
        logs: boolean
            If True, the Gaussian process is used to smooth the natural
            logarithm of the data and the time-derivative is therefore of the
            logarithm of the data.
        noruns: integer, optional
            The number of attempts to be made at optimising the kernel's
            hyperparmeters.
        noinits: integer, optional
            The number of random attempts made to find good initial choices for
            the hyperparameters before running their optimisation.
        exitearly: boolean, optional
            If True, stop at the first successful attempt at optimising the
            hyperparameters otherwise take the best choice from all successful
            optimisations.
        bd: dictionary, optional
            Specifies the limits on the hyperparameters for the Gaussian process.
            For example, bd= {0: [-1, 4], 2: [2, 6]})
            sets confines the first hyperparameter to be between 1e-1 and 1e^4
            and confines the third hyperparmater between 1e2 and 1e6.
        empirical_errors: boolean, optional
            If True, measurement errors are empirically estimated by the
            variance across replicates at each time point.
            If False, the variance of the measurement error is assumed to be
            the same for all time points and its magnitude is a hyperparameter
            that is optimised.
        optmethod: string, optional
            The algorithm used to optimise the hyperparameters, either
            'l_bfgs_b' or 'tnc'.
        warn: boolean, optional
            If False, warnings created by covariance matrices that are not
            positive semi-definite are suppressed.
        linalgmax: integer, optional
            The number of times errors generated by underlying linear algebra
            modules during the optimisation by poor choices of the
            hyperparameters should be ignored.
        max_data_pts: integer, optional
            If set, sufficiently large data sets with multiple replicates will
            be subsampled at each time point, randomly picking a smaller
            number of replicates, to reduce the number of data points and so
            run times.
        """
        self.linalgmax = linalgmax
        self.success = True
        if not runtime_warn:
            # warning generated occasionally when sampling from the Gaussian
            # process likely because of numerical errors
            warnings.simplefilter("ignore", RuntimeWarning)
        try:
            noreps = d.shape[1]
        except IndexError:
            noreps = 1
        self.noreps = noreps
        self.d = np.copy(d)
        self.t = np.copy(t)
        t = self.t
        d = self.d
        # default bounds for hyperparameters
        bddict = {
            "nn": {0: (-1, 5), 1: (-7, -2), 2: (-6, 2)},
            "sqexp": {0: (-5, 5), 1: (-6, 2), 2: (-5, 2)},
            "matern": {0: (-5, 5), 1: (-4, 4), 2: (-5, 2)},
        }
        # find bounds
        if bd:
            self.bds = gu.mergedicts(original=bddict[cvfn], update=bd)
        else:
            self.bds = bddict[cvfn]
        # log data
        self.logs = logs
        if logs:
            print("Taking natural logarithm of the data.")
            if np.any(np.nonzero(d < 0)):
                print("Warning: Negative data is being set to NaN.")
            # replace zeros and negs so that logs can be applied
            d[np.nonzero(d <= 0)] = np.nan
            # take log of data
            d = np.log(np.asarray(d))
        # run checks and define measurement errors
        if empirical_errors:
            # errors must be empirically estimated
            if noreps > 1:
                lod = [
                    np.count_nonzero(np.isnan(d[:, i])) for i in range(noreps)
                ]
                if np.sum(np.diff(lod)) != 0:
                    print(
                        "The replicates have different number of data "
                        "points, but equal numbers of data points are "
                        "needed for empirically estimating errors."
                    )
                    merrors = None
                else:
                    # estimate errors empirically
                    print("Estimating measurement errors empirically.")
                    merrors = gu.findsmoothvariance(d)
            else:
                print("Not enough replicates to estimate errors empirically.")
                merrors = None
        else:
            merrors = None
        self.merrors = merrors
        ta, da, ma, self.success = preprocess_data(t, d, merrors, max_data_pts)
        if self.success:
            self.run(
                cvfn,
                ta,
                da,
                ma,
                noruns,
                noinits,
                exitearly,
                optmethod,
            )

    def run(
        self,
        cvfn,
        ta,
        da,
        ma,
        noruns,
        noinits,
        exitearly,
        optmethod,
    ):
        """Instantiate and run a Gaussian process."""
        try:
            # instantiate GP
            g = getattr(gp, cvfn + "GP")(self.bds, ta, da, merrors=ma)
            print("Using a " + g.description + ".")
            g.info
        except NameError:
            raise Exception("Gaussian process not recognised.")
        # optimise parameters
        g.findhyperparameters(
            noruns,
            noinits=noinits,
            exitearly=exitearly,
            optmethod=optmethod,
            linalgmax=self.linalgmax,
        )
        # display results
        g.results()
        if np.any(ma):
            # check measurement errors
            if len(ma) != len(self.t):
                # NaNs have been removed
                mainterp = interp1d(
                    ta, ma, bounds_error=False, fill_value=(ma[0], ma[-1])
                )
                ma = mainterp(self.t)
        g.predict(self.t, derivs=2, addnoise=True, merrorsnew=ma)
        # results
        self.g = g
        self.logmaxlike = -g.nlml_opt
        self.hparamerr = g.hparamerr
        self.lth = g.lth_opt
        self.f = g.f
        self.df = g.df
        self.ddf = g.ddf
        self.fvar = g.fvar
        self.dfvar = g.dfvar
        self.ddfvar = g.ddfvar

    def fitderivsample(self, nosamples, newt=None):
        """
        Generate samples from the latent function.

        Both values for the latent function and its first two
        derivatives are returned, as a tuple.

        All derivatives must be sampled because by default all are asked
        to be predicted by the underlying Gaussian process.

        Parameters
        ----------
        nosamples: integer
            The number of samples.
        newt: array, optional
            Time points for which the samples should be made.
            If None, the orginal time points are used.

        Returns
        -------
        samples: a tuple of arrays
            The first element of the tuple gives samples of the latent
            function;
            the second element gives samples of the first time derivative; and
            the third element gives samples of the second time derivative.
        """
        if np.any(newt):
            newt = np.asarray(newt)
            # make prediction for new time points
            gps = copy.deepcopy(self.g)
            gps.predict(newt, derivs=2, addnoise=True)
        else:
            gps = self.g
        samples = gps.sample(nosamples, derivs=2)
        return samples

    def plotfit(
        self, char="f", errorfac=1, xlabel="time", ylabel=False, figtitle=False
    ):
        """
        Plot the results of the fitting.

        Either the data and the mean of the optimal Gaussian process or
        the inferred time derivatives are plotted.

        Parameters
        ----------
        char: string
            The variable to plot either 'f' or 'df' or 'ddf'.
        errorfac: float, optional
            The size of the errorbars are errorfac times the standard deviation
            of the optimal Gaussian process.
        ylabel: string, optional
            A label for the y-axis.
        figtitle: string, optional
            A title for the figure.
        """
        x = getattr(self, char)
        xv = getattr(self, char + "var")
        if char == "f":
            d = np.log(self.d) if self.logs else self.d
            plt.plot(self.t, d, "r.")
        plt.plot(self.t, x, "b")
        plt.fill_between(
            self.t,
            x - errorfac * np.sqrt(xv),
            x + errorfac * np.sqrt(xv),
            facecolor="blue",
            alpha=0.2,
        )
        if ylabel:
            plt.ylabel(ylabel)
        else:
            plt.ylabel(char)
        plt.xlabel(xlabel)
        if figtitle:
            plt.title(figtitle)


def subsample_data(d, no_samples_per_time_pt):
    """
    Subsample replicate data.

    At each time point, randomly choose only some of the replicates.
    """
    if d.shape[1] > no_samples_per_time_pt:
        rng = np.random.default_rng()
        nd = rng.choice(d, no_samples_per_time_pt, axis=1, replace=False)
        return nd
    else:
        print(
            f"Number of samples, {no_samples_per_time_pt}, is "
            f"more than or equal to the number of replicates, {d.shape[1]}."
        )
        print("Subsampling stopped.")
        return d


def preprocess_data(t, d, merrors, max_data_pts):
    """Remove nans and make 1D."""
    try:
        noreps = d.shape[1]
    except IndexError:
        noreps = 1
    # subsample if excessive data
    if max_data_pts and d[~np.isnan(d)].size > max_data_pts:
        print(
            f"Many data points - {d[~np.isnan(d)].size}:"
            " subsampling for each time point."
        )
        no_samples_per_time_pt = np.ceil(max_data_pts / d.shape[0]).astype(
            "int"
        )
        d = subsample_data(d, no_samples_per_time_pt)
    # combine data into one array
    tb = np.tile(t, noreps)
    db = np.reshape(d, d.size, order="F")
    # check for NaNs
    if np.any(merrors):
        mb = np.tile(merrors, noreps)
        keep = np.intersect1d(
            np.nonzero(~np.isnan(db))[0], np.nonzero(~np.isnan(mb))[0]
        )
    else:
        keep = np.nonzero(~np.isnan(db))[0]
    # remove any NaNs
    da = db[keep]
    ta = tb[keep]
    # check data remains after removing NaNs
    success = True
    if not da.size:
        print("Warning: omfitderiv failed - too many NaNs.")
        success = False
    elif np.any(merrors):
        # measurement errors
        ma = mb[keep]
        if not ma.size:
            print("Warning: omfitderiv failed - too many NaNs.")
            success = False
    else:
        ma = None
    return ta, da, ma, success
