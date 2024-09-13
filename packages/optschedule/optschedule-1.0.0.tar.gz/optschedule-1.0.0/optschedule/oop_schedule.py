"""
DEPRECATION NOTICE:
Schedule class and object-oriented approach in `optschedule` is deprecated.
Functions and features will remain the same, just make sure to pass `n_steps`
argument to functions individually. Please use scheduling functions directly
(e.g. `from optschedule import exponential_decay`). For more details refer to
'Paradigm Shift' section in the documentation.

=============================================================================

The ``schedule`` module houses ``Schedule`` class that produces sequences that
can be implemented with proprietary and open source optimizers and algorithms.

:raises ValueError: Error if there is more or less than exactly one more element
                    of `values` that `boundaries`
:return: Sequence of values with each element being a value
         (e.g. learning rate or difference) for each epoch
:rtype: ndarray
"""

import numpy as np
import warnings


class Schedule:
    def __init__(self, n_steps) -> None:
        """
        Initializes Schedule Object.

        Object properties:

        - ``n_steps`` - number of steps
        - ``steps`` - sequence of steps

        :param n_steps: Number of decay steps. Must be equal to the number of
                        epochs of the algorithm
        :type n_steps: int
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import exponential_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        self.n_steps = n_steps
        self.steps = np.linspace(0, n_steps, n_steps)

    def exponential_decay(self, initial_value, decay_rate, staircase=False):
        """
        Sequence with exponential decay.

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param decay_rate: Rate of decay
        :type decay_rate: float
        :param staircase: If True decay the sequence at discrete
                          intervals, defaults to False
        :type staircase: bool, optional
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import exponential_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        if staircase is True:
            sequence = initial_value * np.power(
                decay_rate, np.floor(np.divide(self.steps, self.n_steps))
            )
        else:
            sequence = initial_value * np.power(
                decay_rate, np.divide(self.steps, self.n_steps)
            )

        return sequence

    def cosine_decay(self, initial_value, alpha):
        """
        Sequence with cosine decay.

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param alpha: Minimum sequence value as a fraction of initial_value
        :type alpha: float
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import cosine_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        steps = np.minimum(self.steps, self.n_steps)
        cosine_decay = 0.5 * (
            1 + np.cos(np.multiply(np.pi, np.divide(steps, self.n_steps)))
        )
        decayed = (1 - alpha) * cosine_decay + alpha

        sequence = initial_value * decayed

        return sequence

    def inverse_time_decay(self, initial_value, decay_rate, staircase=False):
        """
        Sequence with inverse time decay

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param decay_rate: Rate of decay
        :type decay_rate: float
        :param staircase: If True decay the sequence at discrete
                          intervals, defaults to False
        :type staircase: bool, optional
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import inverse_time_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        if staircase is True:
            sequence = np.divide(
                initial_value,
                (
                    1
                    + np.multiply(
                        decay_rate, np.floor(np.divide(self.steps, self.n_steps))
                    )
                ),
            )
        else:
            sequence = np.divide(
                initial_value,
                (1 + np.multiply(decay_rate, np.divide(self.steps, self.n_steps))),
            )

        return sequence

    def polynomial_decay(self, initial_value, end_value, power, cycle=False):
        """
        Sequence with polynomial decay.

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param end_value: The minimal end sequence value
        :type end_value: float
        :param power: The power of the polynomial
        :type power: float
        :param cycle: Whether or not it should cycle beyond
                      self.n_steps, defaults to False
        :type cycle: bool, optional
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import polynomial_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        if cycle is True:
            n_steps = np.multiply(
                self.n_steps, np.ceil(np.divide(self.steps, self.n_steps))
            )
            sequence = (
                np.multiply(
                    (initial_value - end_value),
                    (np.power(1 - np.divide(self.steps, n_steps), power)),
                )
                + end_value
            )
        else:
            steps = np.minimum(self.steps, self.n_steps)
            sequence = (
                np.multiply(
                    (initial_value - end_value),
                    (np.power(1 - np.divide(steps, self.n_steps), power)),
                )
                + end_value
            )

        return sequence

    def piecewise_constant_decay(self, boundaries, values):
        """
        Sequence with piecewise constant decay.

        :param boundaries: Boundaries of the pieces
        :type boundaries: list
        :param values: list of values in sequence in each of the pieces
        :type values: list
        :raises ValueError: Error if there is more or less than exactly
                            one more element of `values` that `boundaries`
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import piecewise_constant_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        if len(boundaries) + 1 != len(values):
            raise ValueError(
                "There should be only one value for each piece of array, i.e. \
                there should be exactly one more element of `values` that `boundaries`"
            )

        boundaries = np.append(0, boundaries)
        boundaries = np.append(boundaries, self.n_steps)

        sequence = np.zeros(self.n_steps)
        for value in range(len(values)):
            sequence[boundaries[value] : boundaries[value + 1]] = np.full(
                boundaries[value + 1] - boundaries[value], values[value]
            )

        return sequence

    def constant(self, value):
        """
        Constant sequence

        :param value: Value for each epoch
        :type value: float
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import constant`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        sequence = np.full(len(self.steps), value)

        return sequence

    def geometric_decay(self, initial_value, decay_rate, minimum_value):
        """
        Sequence with geometric decay given by

        .. math::
            \\text{value} = \max(\\text{initial_value} \\times \\text{decay_rate}^{\\text{i}}, \\text{minimum_value})

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param decay_rate: Rate of geometric decay
        :type decay_rate: float
        :param minimum_value: Minimum value of the sequence
        :type minimum_value: float
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import geometric_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )
        sequence = np.zeros(self.n_steps)
        sequence[0] = initial_value
        for i in range(self.n_steps - 1):
            sequence[i + 1] = np.maximum(initial_value * decay_rate**i, minimum_value)

        return sequence

    def arithmetic_decay(self, initial_value, decay_rate, minimum_value):
        """
        Sequence with arithmetic decay given by

        .. math::
            \\text{value} = \max(\\text{initial_value} - \\text{decay_rate} \\times \\text{i}, \\text{minimum_value})

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param decay_rate: Rate of arithmetic decay
        :type decay_rate: float
        :param minimum_value: Minimum value of the sequence
        :type minimum_value: float
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import arithmetic_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        sequence = np.zeros(self.n_steps)
        sequence[0] = initial_value
        for i in range(self.n_steps - 1):
            sequence[i + 1] = np.maximum(initial_value - decay_rate * i, minimum_value)

        return sequence

    def time_decay(self, initial_value, decay_rate):
        """
        Sequence with time-based decay given by

        .. math::
            \\text{value} = \\frac{\\text{prev_value}}{1+\\text{decay_rate} \\times \\text{i}}

        where `prev_value` is the previous value in the sequence and
        `decay_rate` is the decay rate parameter.

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param decay_rate: Decay rate
        :type decay_rate: float
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import time_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        sequence = np.zeros(self.n_steps)
        sequence[0] = initial_value
        for i in range(self.n_steps - 1):
            sequence[i + 1] = sequence[i] / (1 + decay_rate * i)

        return sequence

    def step_decay(self, initial_value, decay_value, decay_every):
        """
        Sequence with step decay given by

        .. math::
            \\text{value} = \\text{initial_value} \\times \\text{decay_value}^{\lfloor \\frac{i}{\\text{decay_every}} \\rfloor}

        where `i` is the current value in the sequence.

        :param initial_value: Initial value of the sequence
        :type initial_value: float
        :param decay_value: Drop size
        :type decay_value: float
        :param decay_every: Drop is performed every `decay_every` values
        :type decay_every: int
        :return: Sequence of values with each element being a value
                 (e.g. learning rate or difference) for each epoch
        :rtype: ndarray
        """

        warnings.warn(
            "Schedule class and object-oriented approach in `optschedule` is deprecated. \
        Functions and features will remain the same, just make sure to pass `n_steps` \
        argument to functions individually. Please use scheduling functions directly \
        (e.g. `from optschedule import step_decay`). For more details refer to \
        'Paradigm Shift' section in the documentation.",
            DeprecationWarning,
            stacklevel=2,
        )

        sequence = np.zeros(self.n_steps)
        sequence[0] = initial_value
        for i in range(self.n_steps - 1):
            sequence[i + 1] = initial_value * np.power(
                decay_value, np.floor((1 + i) / decay_every)
            )

        return sequence
