"""
Base implementation of support for plotting during scipy optimisation
"""

from __future__ import annotations

import logging
from collections.abc import Iterable
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Generic,
    Protocol,
)

import more_itertools
import numpy as np
from attrs import define, field
from typing_extensions import TypeAlias

from openscm_calibration.exceptions import (
    MissingValueError,
)
from openscm_calibration.matplotlib_utils import get_fig_axes_holder_from_mosaic
from openscm_calibration.typing import DataContainer

if TYPE_CHECKING:
    import attr
    import matplotlib
    import matplotlib.axes
    import pandas as pd
    import tqdm

    from openscm_calibration.store import OptResStore


logger: logging.Logger = logging.getLogger(__name__)
"""Logger for this module"""


class SupportsScipyOptCallback(Protocol):
    """
    Class that supports being used as a callback with Scipy's optimisers
    """

    def callback_minimize(
        self,
        xk: np.typing.NDArray[np.number[Any]],
    ) -> None:
        """
        Get cost of parameter vector

        This callback is intended to be used with [`scipy.optimize.minimize`][]

        Parameters
        ----------
        xk
            Last used parameter vector
        """

    def callback_differential_evolution(
        self,
        xk: np.typing.NDArray[np.number[Any]],
        convergence: float | None = None,
    ) -> None:
        """
        Get cost of parameter vector

        This callback is intended to be used with
        [`scipy.optimize.differential_evolution`][]

        Parameters
        ----------
        xk
            Parameter vector with best solution found so far

        convergence
            Received from [`scipy.optimize.differential_evolution`][] on callback.
            We are not sure what this does is or is used for.
        """


class SupportsFigUpdate(Protocol):
    """
    Class that supports updating figures

    For example, [`IPython.core.display_functions.DisplayHandle`][]
    """

    def update(
        self,
        obj: Any,
        **kwargs: Any,
    ) -> Any:
        """
        Update the figure

        Parameters
        ----------
        obj
            Figure to update

        **kwargs
            Other arguments used by the updater

        Returns
        -------
        :
            Anything (not used)
        """


ResultsToDictConverter: TypeAlias = Callable[[DataContainer], dict[str, DataContainer]]
"""
Callable used to convert results into a dictionary

This allows us to know which results to plot on which axes
(the keys of the resulting dictionary should match the names of the axes).
"""


class NoSuccessfulRunsError(ValueError):
    """
    Raised when no runs completed successfully i.e. there is nothing to plot
    """


class PlotCostsLike:
    """
    Callable that supports plotting costs
    """

    def __call__(  # noqa: PLR0913
        self,
        ax: matplotlib.axes.Axes,
        ylabel: str,
        costs: tuple[float, ...],
        ymin: float = 0.0,
        get_ymax: Callable[[tuple[float, ...]], float] | None = None,
        alpha: float = 0.7,
        **kwargs: Any,
    ) -> None:
        r"""
        Plot cost function

        Parameters
        ----------
        ax
            Axes on which to plot

        ylabel
            y-axis label

        costs
            Costs to plot

        ymin
            Minimum y-axis value

        get_ymax
            Function which gets the y-max based on the costs. If not provided,
            :func:`get_ymax_default` is used

        alpha
            Alpha to apply to plotted points

        **kwargs
            Passed to :meth:`ax.scatter`
        """


class PlotParametersLike:
    """
    Callable that supports plotting parameters
    """

    def __call__(
        self,
        axes: dict[str, matplotlib.axes.Axes],
        para_vals: dict[str, np.typing.NDArray[np.number[Any]]],
        alpha: float = 0.7,
        **kwargs: Any,
    ) -> None:
        """
        Plot parameters

        Parameters
        ----------
        axes
            Axes on which to plot.

            The keys should match the keys in `para_vals`.

        para_vals
            Parameter values.

            Each key should be the name of a parameter.

        alpha
            Alpha to use when calling [`matplotlib.axes.Axes.scatter`][].

        **kwargs
            Passed to each call to [`matplotlib.axes.Axes.scatter`][].
        """


class PlotTimeseriesLike(Protocol[DataContainer]):
    """
    Callable that supports plotting timeseries
    """

    def __call__(  # noqa: PLR0913
        self,
        best_run: DataContainer,
        others_to_plot: tuple[DataContainer, ...],
        target: DataContainer,
        convert_results_to_plot_dict: ResultsToDictConverter[DataContainer],
        timeseries_keys: Iterable[str],
        axes: dict[str, matplotlib.axes.Axes],
        get_timeseries: Callable[[DataContainer], pd.DataFrame],
    ) -> None:
        """
        Plot timeseries

        Parameters
        ----------
        best_run
            Best run from iterations

        others_to_plot
            Other results to plot from iterations

        target
            Target to which we are calibrating

        convert_results_to_plot_dict
            Callable which converts the data into a dictionary
            in which the keys are a subset of the values in `axes`

        timeseries_keys
            Keys of the timeseries to plot

        axes
            Axes on which to plot

        get_timeseries
            Function which converts the data into a
            [`pandas.DataFrame`][] for plotting
        """


def _all_in_axes(
    instance: OptPlotter[Any],
    attribute: attr.Attribute[tuple[str]],
    value: tuple[str],
) -> None:
    """
    Check all values are present in `self.axes`

    Parameters
    ----------
    self
        Object instance

    attribute
        Attribute to check

    value
        Value to check

    Raises
    ------
    ValueError
        Not all elements in `value` are keys in `self.axes`
    """
    values_without_axes = [k for k in value if k not in instance.axes]
    if values_without_axes:
        raise MissingValueError(
            "self.axes",
            vals=list(instance.axes.keys()),
            missing_vals=values_without_axes,
        )


def _compatible_with_convert_and_target(
    instance: OptPlotter[Any],
    attribute: attr.Attribute[tuple[str]],
    value: tuple[str],
) -> None:
    """
    Check that the values are compatible with the target and the results conversion

    Specifically, compatible with `self.target`
    and `self.convert_results_to_plot_dict`

    Parameters
    ----------
    self
        Object instance

    attribute
        Attribute to check

    value
        Value to check

    Raises
    ------
    ValueError
        If the values in `value` are not all keys in the dictionary
        that is returned when `self.convert_results_to_plot_dict`
        is applied to `self.target`.
    """
    target_converted = instance.convert_results_to_plot_dict(instance.target)
    missing_from_target_converted = [k for k in value if k not in target_converted]
    if missing_from_target_converted:
        raise MissingValueError(
            "self.axes",
            vals=list(instance.axes.keys()),
            missing_vals=missing_from_target_converted,
        )


@define
class OptPlotter(Generic[DataContainer]):
    """
    Optimisation progress plotting helper

    This class is an adapter between interfaces required by Scipy's callback arguments
    and updating the plots.
    The class holds all the information required to make useful plots.
    It is intended to be used in interactive Python i.e. to make updating plots.
    """

    holder: SupportsFigUpdate
    """Figure updater, typically [`IPython.core.display_functions.DisplayHandle`][]"""

    fig: matplotlib.figure.Figure
    """Figure on which to plot"""

    axes: dict[str, matplotlib.axes.Axes]
    """
    Dictionary storing axes on which to plot

    The plot of the cost function over time will be plotted on the axes
    with key given by `cost_key`.

    Each parameter will be plotted on the axes with the same key as the parameter
    (as defined in `parameters`).

    The timeseries will be plotted on the axes specified by `timeseries_axes`.
    See docstring of `timeseries_axes` for rules about its values.
    """

    cost_key: str
    """Key for the axes on which the cost function should be plotted"""

    parameters: tuple[str, ...] = field(validator=[_all_in_axes])
    """
    Parameters to be optimised

    This must match the order in which the parameters are handled by the optimiser,
    i.e. it is used to translate the unlabeled array of parameter values
    onto the desired axes.
    """

    timeseries_axes: tuple[str, ...] = field(
        validator=[_all_in_axes, _compatible_with_convert_and_target]
    )
    """
    Axes on which to plot timeseries

    The timeseries in `target` and `store.res`
    are converted into dictionaries using `convert_results_to_plot_dict`.
    The keys of the result of `convert_results_to_plot_dict`
    must match the values in `timeseries_axes`.
    """

    target: DataContainer
    """Target used for optimisation"""

    store: OptResStore[DataContainer]
    """Optimisation result store"""

    convert_results_to_plot_dict: ResultsToDictConverter[DataContainer]
    """
    Callable which converts results into a dictionary
    in which the keys are a subset of the values in `timeseries_axes`
    """

    get_timeseries: Callable[[DataContainer], pd.DataFrame]
    """
    Function which converts data into timeseries.
    """

    plot_timeseries: PlotTimeseriesLike[DataContainer]
    """
    Function that plots our timeseries
    """

    thin_ts_to_plot: int = 20
    """
    Thinning to apply to the timeseries to plot

    In other words, only plot every `thin_ts_to_plot` runs on the timeseries plots.
    Plotting all runs can be very expensive.
    """

    plot_costs: PlotCostsLike | None = None
    """
    Function that plots our costs

    If not supplied, we use
    [`plot_costs`][openscm_calibration.scipy_plotting.plot_costs].
    """

    plot_parameters: PlotParametersLike | None = None
    """
    Function that plots our parameters

    If not supplied, we use
    [`plot_parameters`][openscm_calibration.scipy_plotting.plot_parameters].
    """

    def callback_minimize(
        self,
        xk: np.typing.NDArray[np.number[Any]],
    ) -> None:
        """
        Update the plots

        Intended to be used as the `callback` argument to
        [`scipy.optimize.minimize`][].

        Parameters
        ----------
        xk
            Last used parameter vector
        """
        self.update_plots()

    def callback_differential_evolution(
        self,
        xk: np.typing.NDArray[np.number[Any]],
        convergence: float | None = None,
    ) -> None:
        """
        Update the plots

        Intended to be used as the `callback` argument to
        `scipy.optimize.differential_evolution`

        Parameters
        ----------
        xk
            Parameter vector with best solution found so far

        convergence
            Received from [`scipy.optimize.differential_evolution`][] on callback.
            We are not sure what this does is or what it is used for.
        """
        self.update_plots()

    @classmethod
    def from_autogenerated_figure(  # noqa: PLR0913
        cls,
        cost_key: str,
        params: tuple[str],
        convert_results_to_plot_dict: ResultsToDictConverter[DataContainer],
        target: DataContainer,
        store: OptResStore[DataContainer],
        kwargs_create_mosaic: dict[str, Any] | None = None,
        kwargs_get_fig_axes_holder: dict[str, Any] | None = None,
        **kwargs: Any,
    ) -> OptPlotter[DataContainer]:
        """
        Create plotter with automatic figure generation

        Parameters
        ----------
        cost_key
            Name to use for the cost axis

        params
            Parameters that are being optimised

            This is used to generate the plotting axes.
            It must also match the order in which the parameters are handled by the optimiser,
            i.e. it is used to translate the unlabeled array of parameter values
            onto the desired axes.

        convert_results_to_plot_dict
            Callable which converts results into a dictionary

        target
            Target to which we are optimising

        store
            Optimisation result store

        kwargs_create_mosaic
            Passed to [`get_optimisation_mosaic`][openscm_calibration.scipy_plotting.get_optimisation_mosaic]

        kwargs_get_fig_axes_holder
            Passed to [`get_fig_axes_holder_from_mosaic`][openscm_calibration.matplotlib_utils.get_fig_axes_holder_from_mosaic]

        **kwargs
            Passed to the initialiser of [`OptPlotter`][openscm_calibration.scipy_plotting.OptPlotter]

        Returns
        -------
        :
            Initialised instance with generated figure, axes and holder
        """  # noqa: E501
        if kwargs_create_mosaic is None:
            kwargs_create_mosaic = {}

        if kwargs_get_fig_axes_holder is None:
            kwargs_get_fig_axes_holder = {}

        timeseries_axes = tuple(convert_results_to_plot_dict(target).keys())
        mosaic = get_optimisation_mosaic(
            cost_key=cost_key,
            params=params,
            timeseries=timeseries_axes,
            **kwargs_create_mosaic,
        )

        fig, axes, holder = get_fig_axes_holder_from_mosaic(
            mosaic, **kwargs_get_fig_axes_holder
        )

        return cls(
            holder=holder,
            fig=fig,
            axes=axes,
            cost_key=cost_key,
            parameters=params,
            timeseries_axes=timeseries_axes,
            convert_results_to_plot_dict=convert_results_to_plot_dict,
            target=target,
            store=store,
            **kwargs,
        )

    def update_plots(self) -> None:
        """
        Update all the plots
        """
        costs, para_vals, res = self.store.get_costs_labelled_xsamples_res()

        # check if anything to plot
        if np.all(~np.isfinite(costs)):
            logger.info("No runs succeeded, nothing to plot")
            return

        # plot cost function
        ax_cost = self.axes[self.cost_key]
        ax_cost.clear()

        if self.plot_costs is None:
            plot_costs_h = plot_costs
        else:
            plot_costs_h = self.plot_costs

        plot_costs_h(ax=ax_cost, ylabel=self.cost_key, costs=costs)

        # plot parameters
        for parameter in self.parameters:
            self.axes[parameter].clear()

        if self.plot_parameters is None:
            plot_parameters_h = plot_parameters
        else:
            plot_parameters_h = self.plot_parameters

        plot_parameters_h(axes=self.axes, para_vals=para_vals)

        # plot timeseries
        best_run, others_to_plot = get_runs_to_plot(costs, res, self.thin_ts_to_plot)

        for k in self.timeseries_axes:
            self.axes[k].clear()

        self.plot_timeseries(
            best_run=best_run,
            others_to_plot=others_to_plot,
            target=self.target,
            convert_results_to_plot_dict=self.convert_results_to_plot_dict,
            timeseries_keys=self.timeseries_axes,
            axes=self.axes,
            get_timeseries=self.get_timeseries,
        )

        # update and return
        self.fig.tight_layout()
        self.holder.update(self.fig)


def plot_costs(  # noqa: PLR0913
    ax: matplotlib.axes.Axes,
    ylabel: str,
    costs: tuple[float, ...],
    ymin: float = 0.0,
    get_ymax: Callable[[tuple[float, ...]], float] | None = None,
    alpha: float = 0.7,
    **kwargs: Any,
) -> None:
    r"""
    Plot cost function

    Parameters
    ----------
    ax
        Axes on which to plot

    ylabel
        y-axis label

    costs
        Costs to plot

    ymin
        Minimum y-axis value

    get_ymax
        Function which gets the y-max based on the costs. If not provided,
        :func:`get_ymax_default` is used

    alpha
        Alpha to apply to plotted points

    **kwargs
        Passed to :meth:`ax.scatter`
    """
    if get_ymax is None:
        get_ymax = get_ymax_default

    ax.scatter(range(len(costs)), costs, alpha=alpha, **kwargs)
    ax.set_ylabel(ylabel)

    ymax = get_ymax(costs)
    if not np.isfinite(ymax):
        ymax = 10**3

    ax.set_ylim(
        ymin=ymin,
        ymax=ymax,
    )


def get_ymax_default(
    costs: tuple[float, ...],
    min_scale_factor: float = 10.0,
    min_v_median_scale_factor: float = 2.0,
) -> float:
    r"""
    Get y-max based on costs

    This is the default function used by
    [`plot_costs`][openscm_calibration.scipy_plotting.base.plot_costs].
    The algorithm is

    .. math::

        \text{ymax} = min(
            \text{min_scale_factor} \times min(costs),
            max(
                median(costs),
                \text{min_v_median_scale_factor} \times min(costs)
            )
        )

    Parameters
    ----------
    costs
        Cost function values

    min_scale_factor
        Value by which the minimum value is scaled when determining the plot
        limits

    min_v_median_scale_factor
        Value by which the minimum value is scaled when comparing to the
        median as part of determining the plot limits

    Returns
    -------
        Maximum value to use on the y-axis
    """
    min_cost = np.min(costs)
    ymax = np.min(
        [
            min_scale_factor * min_cost,
            np.max([np.median(costs), min_v_median_scale_factor * min_cost]),
        ]
    )

    return float(ymax)


def plot_parameters(
    axes: dict[str, matplotlib.axes.Axes],
    para_vals: dict[str, np.typing.NDArray[np.number[Any]]],
    alpha: float = 0.7,
    **kwargs: Any,
) -> None:
    """
    Plot parameters

    Parameters
    ----------
    axes
        Axes on which to plot. The keys should match the keys in ``para_vals``

    para_vals
        Parameter values. Each key should be the name of a parameter

    alpha
        Alpha to use when calling :meth:`matplotlib.axes.Axes.scatter`

    **kwargs
        Passed to each call to :meth:`matplotlib.axes.Axes.scatter`
    """
    for parameter, values in para_vals.items():
        axes[parameter].scatter(range(len(values)), values, alpha=alpha, **kwargs)
        axes[parameter].set_ylabel(parameter)


def get_runs_to_plot(
    costs: tuple[float, ...],
    res: tuple[DataContainer, ...],
    thin_ts_to_plot: int,
) -> tuple[DataContainer, tuple[DataContainer, ...]]:
    """
    Get runs to plot

    This retrieves the run which best matches the target (has lowest cost)
    and then a series of others to plot.

    Parameters
    ----------
    costs
        Cost function value for each run (used to determine the best result)

    res
        Results of each run.

        It is assumed that the elements in ``res``
        and ``costs`` line up i.e. the nth element of ``costs``
        is the cost function for the nth element in ``res``.

    thin_ts_to_plot
        Thinning to apply to the timeseries to plot

        In other words, only plot every `thin_ts_to_plot` runs
        on the timeseries plots.
        Plotting all runs can be very expensive.

    Returns
    -------
    :
        Best iteration and other runs to plot

    Raises
    ------
    ValueError
        No successful runs are included in ``res``
    """
    # Convert to dict for quicker lookup later
    res_d_success = {i: v for i, v in enumerate(res) if v is not None}
    if not res_d_success:
        raise NoSuccessfulRunsError()

    best_it = int(np.argmin(costs))
    out_best = res_d_success[best_it]

    success_keys = list(res_d_success.keys())
    to_plot_not_best = success_keys[
        len(success_keys) - 1 :: -thin_ts_to_plot  # (prefer black)
    ]
    if best_it in to_plot_not_best:
        to_plot_not_best.remove(best_it)

    out_not_best = tuple([res_d_success[i] for i in to_plot_not_best])

    return out_best, out_not_best


@define
class CallbackProxy(Generic[DataContainer]):
    """
    Callback helper

    This class acts as a proxy and decides whether the real callback should
    actually be called. If provided, it also keeps track of the number of
    model calls via a progress bar.
    """

    real_callback: SupportsScipyOptCallback
    """Callback to be called if a sufficient number of runs have been done"""

    store: OptResStore[DataContainer]
    """Optimisation result store"""

    last_callback_val: int = 0
    """Number of model calls at last callback"""

    update_every: int = 50
    """Update the plots every X calls to the model"""

    progress_bar: tqdm.std.tqdm[Any] | None = None
    """Progress bar to track iterations"""

    def callback_minimize(
        self,
        xk: np.typing.NDArray[np.number[Any]],
    ) -> None:
        """
        Update the plots

        Intended to be used as the `callback` argument to
        `scipy.optimize.minimize`

        Parameters
        ----------
        xk
            Last used parameter vector
        """
        if self.time_to_call_real_callback():
            self.real_callback.callback_minimize(xk)

    def callback_differential_evolution(
        self,
        xk: np.typing.NDArray[np.number[Any]],
        convergence: float | None = None,
    ) -> None:
        """
        Update the plots

        Intended to be used as the `callback` argument to
        `scipy.optimize.differential_evolution`

        Parameters
        ----------
        xk
            Parameter vector with best solution found so far

        convergence
            Received from :func:`scipy.optimize.differential_evolution`
            on callback. Not sure what this does is or is used for.
        """
        if self.time_to_call_real_callback():
            self.real_callback.callback_differential_evolution(xk, convergence)

    def time_to_call_real_callback(self) -> bool:
        """
        Check whether it is time to call the real callback

        Returns
        -------
            ``True`` if the real callback should be called
        """
        n_model_calls = sum(x is not None for x in self.store.x_samples)
        if self.progress_bar:
            self.update_progress_bar(n_model_calls)

        if n_model_calls < self.last_callback_val + self.update_every:
            return False

        # Note that we ran the full callback
        self.last_callback_val = n_model_calls

        return True

    def update_progress_bar(self, n_model_calls: int) -> None:
        """
        Update the progress bar

        Parameters
        ----------
        n_model_calls
            Number of model calls in total

        Raises
        ------
        TypeError
            ``self.progress_bar`` is ``None``. This typically happens if it
            was not set at the time the :obj:`CallbackProxy` was initialised.
        """
        if self.progress_bar is None:
            raise TypeError(self.progress_bar)

        self.progress_bar.update(n_model_calls - self.progress_bar.last_print_n)


def get_optimisation_mosaic(  # noqa: PLR0913
    cost_key: str,
    params: tuple[str, ...],
    timeseries: tuple[str, ...],
    cost_col_relwidth: int = 1,
    n_parameters_per_row: int = 1,
    n_timeseries_per_row: int = 1,
) -> list[list[str]]:
    """
    Get optimisation mosaic

    This gives back the grid of axes to use for plotting. It can be understood
    by matplotlib but in theory could be used with any tool that understands
    such mosaics/grids.

    Parameters
    ----------
    cost_key
        Name to use for the cost axis

    params
        Parameters axes to generate

    timeseries
        Timeseries axes to generate

    cost_col_relwidth
        Width of the cost axis, relative to the width of each parameter axis

    n_parameters_per_row
        Number of parameters to plot per row (as many rows as are needed to
        plot all the parameters are created)

    n_timeseries_per_row
        Number of timeseries to plot per row (as many rows as are needed to
        plot all the timeseries are created)

    Returns
    -------
        Mosaic
    """
    parameters_wrapped = more_itertools.grouper(
        params, n_parameters_per_row, fillvalue="."
    )
    timeseries_axes_wrapped = more_itertools.grouper(
        timeseries, n_timeseries_per_row, fillvalue="."
    )

    n_top_half_cols = cost_col_relwidth + n_parameters_per_row
    n_bottom_half_cols = n_timeseries_per_row

    top_half_row_repeats = [
        ([cost_key] * cost_col_relwidth + list(parameter_row), n_bottom_half_cols)
        for parameter_row in parameters_wrapped
    ]
    bottom_half_row_repeats = [
        (row, n_top_half_cols) for row in timeseries_axes_wrapped
    ]

    mosaic = [
        list(more_itertools.repeat_each(row, n_repeats))
        for row, n_repeats in top_half_row_repeats + bottom_half_row_repeats
    ]

    return mosaic
