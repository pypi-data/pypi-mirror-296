import numpy as np
import numba as nb
import numbers
from inspect import signature
import warnings


def _check_iterables(h, l, epochs, n_parameters):
    if isinstance(h, (int, float)):
        h = np.full((epochs, n_parameters), h)
    elif isinstance(h, (list, nb.typed.List)):
        h = np.array(h)
        if h.shape == (epochs,):
            h = np.full((epochs, n_parameters), h.reshape(epochs, 1))
        elif h.shape == (epochs, 1):
            h = np.full((epochs, n_parameters), h)
        elif h.shape != (epochs, n_parameters):
            raise ValueError(
                "`h.shape` is invalid. Please provide differences `h` in form of a constant, or array-like of shape (epochs,) or (epochs, n_parameters)"
            )
    elif isinstance(h, np.ndarray):
        if h.shape == (epochs,):
            h = np.full((epochs, n_parameters), h.reshape(epochs, 1))
        elif h.shape == (epochs, 1):
            h = np.full((epochs, n_parameters), h)
        elif h.shape != (epochs, n_parameters):
            raise ValueError(
                "`h.shape` is invalid. Please provide differences `h` in form of a constant, or array-like of shape (epochs,) or (epochs, n_parameters)"
            )
    else:
        raise ValueError(
            "Differences should be of type `int`, `float`, `list`, `nb.typed.List` or `np.ndarray`"
        )

    if isinstance(l, (int, float)):
        l = np.full((epochs, n_parameters), l)
    elif isinstance(l, (list, nb.typed.List)):
        l = np.array(l)
        if l.shape == (epochs,):
            l = np.full((epochs, n_parameters), l.reshape(epochs, 1))
        elif l.shape == (epochs, 1):
            l = np.full((epochs, n_parameters), l)
        elif l.shape != (epochs, n_parameters):
            raise ValueError(
                "`l.shape` is invalid. Please provide learning rate(s) `l` in form of a constant, or array-like of shape (epochs,) or (epochs, n_parameters)"
            )
    elif isinstance(l, np.ndarray):
        if l.shape == (epochs,):
            l = np.full((epochs, n_parameters), l.reshape(epochs, 1))
        elif l.shape == (epochs, 1):
            l = np.full((epochs, n_parameters), l)
        elif l.shape != (epochs, n_parameters):
            raise ValueError(
                "`l.shape` is invalid. Please provide learning rate(s) `l` in form of a constant, or array-like of shape (epochs,) or (epochs, n_parameters)"
            )
    else:
        raise ValueError(
            "Learning rates should be of type `int`, `float`, `list`, `nb.typed.List` or `np.ndarray`"
        )

    if not isinstance(epochs, int):
        raise ValueError("Number of epochs should be an integer")
    if epochs < 1:
        raise ValueError("Number of epochs should be positive")

    if h.shape[0] != l.shape[0]:
        raise ValueError("Number of differences and learning rates should be equal.")
    if epochs != h.shape[0]:
        raise ValueError(
            "Number of epochs, differences and learning rates given should be equal."
        )

    return h, l


def _check_objective(objective, parameters, metaparameters, numba):
    if not callable(objective):
        raise ValueError(
            f"Objective function should be a callable. Current objective function type is:{type(objective)}"
        )

    if numba and not isinstance(objective, nb.core.dispatcher.Dispatcher):
        raise ValueError(
            "`numba=True`, but the objective is not wrapped by one of the `Numba` `@jit` decorators, (e.g. `numba.jit`, `numba.njit`). If you wish to use `numba=True`, make sure to wrap the ***`Numba` compatible objective function*** by one of the `Numba` `@jit` decorators"
        )

    n_arguments = len(signature(objective).parameters)
    if n_arguments > 2:
        raise ValueError(
            "Objective function should take at most 2 arguments, one for `parameters` (required) and one for `metaparameters` (optional)"
        )

    try:
        outputs = objective(parameters)
        no_metaparameters = True
    except TypeError:
        outputs = objective(parameters, metaparameters)
        no_metaparameters = False
    if isinstance(outputs, numbers.Number):
        n_outputs = 1
        output_is_number = True
    else:
        n_outputs = len(outputs)
        output_is_number = False

    return n_outputs, output_is_number, no_metaparameters


def _check_arguments(
    initial=None,
    parameters_used=None,
    momentum=None,
    threads=None,
    rng_seed=None,
    partial_epochs=None,
    total_epochs=None,
    outputs=None,
    parameters=None,
    metaparameters=None,
    columns=None,
    numba=None,
):
    if isinstance(initial, (int, float)):
        initial = np.array([initial])
    elif isinstance(initial, (list, nb.typed.List)):
        initial = np.array(initial)
    elif isinstance(initial, (np.ndarray, type(None))):
        pass
    else:
        raise ValueError(
            "Initial parameters should expressed as either `int`, `float`, `list`, `nb.typed.List` or `np.ndarray`"
        )

    if not isinstance(parameters_used, (int, type(None))):
        raise ValueError("Number of parameters used should be a positive integer")
    if parameters_used is not None:
        if parameters_used < 1:
            raise ValueError("Number of parameters used should be a positive integer")

    if not isinstance(partial_epochs, (int, type(None))):
        raise ValueError("Number of partial epochs should be non-negative integer")
    if partial_epochs is not None:
        if partial_epochs < 0:
            raise ValueError("Number of partial epochs should be non-negative integer")
    if partial_epochs is not None:
        if partial_epochs == 0:
            warnings.warn(
                "Number of partial epochs is 0 (zero). All epochs will be run with regular algorithm",
                UserWarning,
            )

    if not isinstance(total_epochs, (int, type(None))):
        raise ValueError("Number of total epochs should be a positive integer")
    if total_epochs is not None:
        if total_epochs < 1:
            raise ValueError("Number of total epochs should be a positive integer")

    if not isinstance(momentum, (int, float, type(None))):
        raise ValueError("Momentum should be an `int` or a `float`")
    if momentum is not None:
        if momentum < 0:
            raise ValueError("Momentum should be non-negative")

    if not isinstance(threads, (int, type(None))):
        raise ValueError("Number of threads should be a positive integer")
    if threads is not None:
        if threads < 1:
            raise ValueError("Number of threads should be a positive integer")

    if not isinstance(rng_seed, (int, type(None))):
        raise ValueError("RNG seed should be a non-negative integer")
    if rng_seed is not None:
        if rng_seed < 0:
            raise ValueError("RNG seed should be a non-negative integer")

    if not isinstance(outputs, (list, np.ndarray, type(None))):
        raise ValueError("Outputs should be of type `list` or `np.ndarray`")
    try:
        len_outputs = len(outputs[0])
    except TypeError:
        len_outputs = 1

    if not isinstance(parameters, (list, np.ndarray, type(None))):
        raise ValueError("Parameters should be of type `list` or `np.ndarray`")
    try:
        len_parameters = len(parameters[0])
    except TypeError:
        len_parameters = 1

    if not isinstance(metaparameters, (list, nb.typed.List, np.ndarray, type(None))):
        raise ValueError(
            "`metaparameters` should be of type `list`, `nb.typed.List`, `np.ndarray` or `NoneType`"
        )
    if numba and isinstance(metaparameters, list):
        metaparameters = np.array(metaparameters)
        warnings.warn(
            "In `numba=True` mode lists are converted into `Numpy` arrays, which are homogenous data structures (all elements are of the same data type). If your metaparameters have varying data types, list-to-array conversion will make them all strings. This can and should be handled inside the objective function by unpacking metaparameters argument and converting different metaparameters into each own data type separately. Alternatively, use Numpy Structured Arrays (more info at: numpy.org/doc/stable/user/basics.rec.html#structured-arrays)."
        )
    elif isinstance(metaparameters, nb.typed.List):
        metaparameters = np.array(metaparameters)
    if isinstance(metaparameters, type(None)):
        len_metaparameters = 0
    elif isinstance(metaparameters, (list, nb.typed.List, np.ndarray)):
        len_metaparameters = len(metaparameters)

    if not isinstance(columns, (list, np.ndarray, type(None))):
        raise ValueError("Columns should be either a `list` or `np.ndarray`")

    if outputs is not None and parameters is not None and columns is not None:
        if (len_outputs + len_parameters + len_metaparameters) != len(columns):
            raise ValueError(
                "Number of column names given in `columns` doesn't match the combined number of outputs, parameters and columns"
            )

    return initial, metaparameters


def _check_threads(threads, parameters):
    if isinstance(parameters, int):
        if parameters + 1 != threads:
            raise ValueError(
                "Each parameter should have only one CPU thread, along with one for the base evaluation."
            )
    elif len(parameters[0]) + 1 != threads:
        raise ValueError(
            "Each parameter should have only one CPU thread, along with one for the base evaluation."
        )


def _check_numba(numba):
    if not isinstance(numba, bool):
        raise ValueError(
            "`numba` argument specifies whether the algorithm will use `Numba` JIT compiler or Python interpreter, and should be of type `bool`"
        )
