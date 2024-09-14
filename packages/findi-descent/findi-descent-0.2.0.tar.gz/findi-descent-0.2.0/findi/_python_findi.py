"""
Module `_python_findi` stores functions that will be used for optimization
if the user chooses `numba=False` in public functions stored in `findi` module.
These are regular `Python` functions that will use `Python` interpreter for
evaluation and do not require any particular formatting of an objective function.
Parallelization is possible using the `joblib` library. Detailed docstrings
are omitted, as they are provided in `findi` module.
"""

import numpy as np
import pandas as pd
from joblib import Parallel, delayed
import findi._checks


def _update(
    rate,
    difference_objective,
    outputs,
    difference,
    momentum,
    velocity,
    epoch,
    parameters,
):
    # Updated parameter values

    velocity = (
        momentum * velocity
        - rate * (difference_objective - outputs[epoch, 0]) / difference
    )
    updated_parameters = parameters[epoch] + velocity

    return updated_parameters, velocity


def _python_descent(
    objective,
    initial,
    h,
    l,
    epochs,
    metaparameters=None,
    momentum=0,
    threads=1,
    numba=False,
):
    # Performs the regular Gradient Descent using Python interpreter for evaluation

    initial, metaparameters = findi._checks._check_arguments(
        initial=initial,
        momentum=momentum,
        threads=threads,
        metaparameters=metaparameters,
        numba=numba,
    )
    n_outputs, output_is_number, no_metaparameters = findi._checks._check_objective(
        objective, initial, metaparameters, numba
    )
    (h, l) = findi._checks._check_iterables(h, l, epochs, initial.shape[0])

    n_parameters = initial.shape[0]
    outputs = np.zeros([epochs, n_outputs])
    parameters = np.zeros([epochs + 1, n_parameters])
    parameters[0] = initial
    difference_objective = np.zeros(n_parameters)
    velocity = 0

    if threads == 1:
        for epoch, (rate, difference) in enumerate(zip(l, h)):
            if output_is_number:
                if no_metaparameters:
                    outputs[epoch] = objective(parameters[epoch])

                    for parameter in range(n_parameters):
                        current_parameters = parameters[epoch]
                        current_parameters[parameter] = (
                            current_parameters[parameter] + difference[parameter]
                        )

                        difference_objective[parameter] = objective(current_parameters)
                else:
                    outputs[epoch] = objective(parameters[epoch], metaparameters)

                    for parameter in range(n_parameters):
                        current_parameters = parameters[epoch]
                        current_parameters[parameter] = (
                            current_parameters[parameter] + difference[parameter]
                        )

                        difference_objective[parameter] = objective(
                            current_parameters, metaparameters
                        )
            else:
                if no_metaparameters:
                    outputs[epoch] = objective(parameters[epoch])

                    for parameter in range(n_parameters):
                        current_parameters = parameters[epoch]
                        current_parameters[parameter] = (
                            current_parameters[parameter] + difference[parameter]
                        )

                        difference_objective[parameter] = objective(current_parameters)[
                            0
                        ]
                else:
                    outputs[epoch] = objective(parameters[epoch], metaparameters)

                    for parameter in range(n_parameters):
                        current_parameters = parameters[epoch]
                        current_parameters[parameter] = (
                            current_parameters[parameter] + difference[parameter]
                        )

                        difference_objective[parameter] = objective(
                            current_parameters, metaparameters
                        )[0]

            parameters[epoch + 1], velocity = _update(
                rate,
                difference_objective,
                outputs,
                difference,
                momentum,
                velocity,
                epoch,
                parameters,
            )

    elif threads > 1:
        findi._checks._check_threads(threads, parameters)

        current_parameters = np.zeros([n_parameters + 1, n_parameters])

        for epoch, (rate, difference) in enumerate(zip(l, h)):
            current_parameters[0] = parameters[epoch]
            for parameter in range(n_parameters):
                current_parameters[parameter + 1] = parameters[epoch]
                current_parameters[parameter + 1, parameter] = (
                    current_parameters[0, parameter] + difference[parameter]
                )
            if no_metaparameters:
                parallel_outputs = Parallel(n_jobs=threads)(
                    delayed(objective)(i) for i in current_parameters
                )
            else:
                parallel_outputs = Parallel(n_jobs=threads)(
                    delayed(objective)(i, metaparameters) for i in current_parameters
                )

            outputs[epoch] = parallel_outputs[0]

            if output_is_number:
                difference_objective = np.array(
                    [parallel_outputs[i] for i in range(1, n_parameters + 1)]
                )
            else:
                difference_objective = np.array(
                    [parallel_outputs[i][0] for i in range(1, n_parameters + 1)]
                )

            parameters[epoch + 1], velocity = _update(
                rate,
                difference_objective,
                outputs,
                difference,
                momentum,
                velocity,
                epoch,
                parameters,
            )

    return outputs, parameters[:-1]


def _python_partial_descent(
    objective,
    initial,
    h,
    l,
    epochs,
    parameters_used,
    metaparameters=None,
    momentum=0,
    threads=1,
    rng_seed=88,
    numba=False,
):
    # Performs Partial Gradient Descent using Python interpreter for evaluation

    initial, metaparameters = findi._checks._check_arguments(
        initial=initial,
        parameters_used=parameters_used,
        momentum=momentum,
        threads=threads,
        rng_seed=rng_seed,
        metaparameters=metaparameters,
        numba=numba,
    )
    n_outputs, output_is_number, no_metaparameters = findi._checks._check_objective(
        objective, initial, metaparameters, numba
    )
    (h, l) = findi._checks._check_iterables(h, l, epochs, initial.shape[0])

    n_parameters = initial.shape[0]
    outputs = np.zeros([epochs, n_outputs])
    parameters = np.zeros([epochs + 1, n_parameters])
    parameters[0] = initial
    difference_objective = np.zeros(n_parameters)
    rng = np.random.default_rng(rng_seed)
    velocity = 0

    if threads == 1:
        for epoch, (rate, difference) in enumerate(zip(l, h)):
            param_idx = rng.integers(low=0, high=n_parameters, size=parameters_used)

            if output_is_number:
                if no_metaparameters:
                    outputs[epoch] = objective(parameters[epoch])

                    for parameter in range(n_parameters):
                        if parameter in param_idx:
                            current_parameters = parameters[epoch]
                            current_parameters[parameter] = (
                                current_parameters[parameter] + difference[parameter]
                            )

                            difference_objective[parameter] = objective(
                                current_parameters
                            )
                        else:
                            difference_objective[parameter] = outputs[epoch]
                else:
                    outputs[epoch] = objective(parameters[epoch], metaparameters)

                    for parameter in range(n_parameters):
                        if parameter in param_idx:
                            current_parameters = parameters[epoch]
                            current_parameters[parameter] = (
                                current_parameters[parameter] + difference[parameter]
                            )

                            difference_objective[parameter] = objective(
                                current_parameters, metaparameters
                            )
                        else:
                            difference_objective[parameter] = outputs[epoch]
            else:
                if no_metaparameters:
                    outputs[epoch] = objective(parameters[epoch])

                    for parameter in range(n_parameters):
                        if parameter in param_idx:
                            current_parameters = parameters[epoch]
                            current_parameters[parameter] = (
                                current_parameters[parameter] + difference[parameter]
                            )

                            difference_objective[parameter] = objective(
                                current_parameters
                            )[0]
                        else:
                            difference_objective[parameter] = outputs[epoch, 0]
                else:
                    outputs[epoch] = objective(parameters[epoch], metaparameters)

                    for parameter in range(n_parameters):
                        if parameter in param_idx:
                            current_parameters = parameters[epoch]
                            current_parameters[parameter] = (
                                current_parameters[parameter] + difference[parameter]
                            )

                            difference_objective[parameter] = objective(
                                current_parameters, metaparameters
                            )[0]
                        else:
                            difference_objective[parameter] = outputs[epoch, 0]

            parameters[epoch + 1], velocity = _update(
                rate,
                difference_objective,
                outputs,
                difference,
                momentum,
                velocity,
                epoch,
                parameters,
            )

    elif threads > 1:
        findi._checks._check_threads(threads, parameters_used)

        current_parameters = np.zeros([n_parameters + 1, n_parameters])

        for epoch, (rate, difference) in enumerate(zip(l, h)):
            param_idx = rng.integers(low=0, high=n_parameters, size=parameters_used)

            current_parameters[0] = parameters[epoch]
            for parameter in range(n_parameters):
                current_parameters[parameter + 1] = parameters[epoch]
                if parameter in param_idx:
                    current_parameters[parameter + 1, parameter] = (
                        current_parameters[0, parameter] + difference[parameter]
                    )

            if no_metaparameters:
                parallel_outputs = Parallel(n_jobs=threads)(
                    delayed(objective)(i)
                    for i in current_parameters[
                        np.append(np.array([0]), np.add(param_idx, 1))
                    ]
                )
            else:
                parallel_outputs = Parallel(n_jobs=threads)(
                    delayed(objective)(i, metaparameters)
                    for i in current_parameters[
                        np.append(np.array([0]), np.add(param_idx, 1))
                    ]
                )

            outputs[epoch] = parallel_outputs[0]

            if output_is_number:
                difference_objective = np.full(n_parameters, parallel_outputs[0])
                difference_objective[param_idx] = np.array(
                    [parallel_outputs[i] for i in range(1, parameters_used + 1)]
                )
            else:
                difference_objective = np.full(n_parameters, parallel_outputs[0][0])
                difference_objective[param_idx] = np.array(
                    [parallel_outputs[i][0] for i in range(1, parameters_used + 1)]
                )

            parameters[epoch + 1], velocity = _update(
                rate,
                difference_objective,
                outputs,
                difference,
                momentum,
                velocity,
                epoch,
                parameters,
            )

    return outputs, parameters[:-1]


def _python_partially_partial_descent(
    objective,
    initial,
    h,
    l,
    partial_epochs,
    total_epochs,
    parameters_used,
    metaparameters=None,
    momentum=0,
    threads=1,
    rng_seed=88,
):
    # Performs Partially Partial Gradient Descent using Python interpreter for evaluation

    initial, metaparameters = findi._checks._check_arguments(
        initial=initial,
        partial_epochs=partial_epochs,
        total_epochs=total_epochs,
        metaparameters=metaparameters,
    )
    (h, l) = findi._checks._check_iterables(h, l, total_epochs, initial.shape[0])

    outputs_p, parameters_p = _python_partial_descent(
        objective=objective,
        initial=initial,
        h=h[:partial_epochs],
        l=l[:partial_epochs],
        epochs=partial_epochs,
        parameters_used=parameters_used,
        metaparameters=metaparameters,
        momentum=momentum,
        threads=threads,
        rng_seed=rng_seed,
    )

    outputs_r, parameters_r = _python_descent(
        objective=objective,
        initial=parameters_p[-1],
        h=h[partial_epochs:],
        l=l[partial_epochs:],
        epochs=(total_epochs - partial_epochs),
        momentum=momentum,
        threads=threads,
        metaparameters=metaparameters,
    )

    outputs = np.append(outputs_p, outputs_r)
    parameters = np.append(parameters_p, parameters_r)
    outputs = np.reshape(outputs, newshape=[-1, 1])
    parameters = np.reshape(parameters, newshape=[-1, 1])

    return outputs, parameters


def values_out(outputs, parameters, metaparameters=None, columns=None):
    # Compiles outputs, parameters and metaparameters into a Pandas DataFrame

    findi._checks._check_arguments(
        outputs=outputs,
        parameters=parameters,
        metaparameters=metaparameters,
        columns=columns,
    )

    if columns is None:
        columns = np.array([], dtype=np.str_)
    if metaparameters is None:
        metaparameters = np.array([])

    if len(metaparameters) == 0:
        inputs = parameters
    else:
        inputs = np.concatenate(
            [
                parameters,
                np.full(
                    (len(parameters), len(metaparameters)),
                    metaparameters,
                ),
            ],
            axis=1,
            dtype=np.str_,
        )

    values = pd.DataFrame(
        np.concatenate((outputs, inputs), axis=1),
        columns=columns,
    )

    return values.convert_dtypes()
