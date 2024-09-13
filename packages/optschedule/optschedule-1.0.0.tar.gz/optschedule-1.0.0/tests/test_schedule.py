import pytest
from optschedule import *
import numpy as np


def test_exponential():
    rates = exponential_decay(n_steps=10, initial_value=0.1, decay_rate=0.5)

    true_values = np.array(
        [
            0.1,
            0.09258747,
            0.0857244,
            0.07937005,
            0.07348672,
            0.0680395,
            0.06299605,
            0.05832645,
            0.05400299,
            0.05,
        ]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_cosine():
    rates = cosine_decay(n_steps=10, initial_value=0.1, alpha=0.1)

    true_values = np.array(
        [
            0.1,
            0.09728617,
            0.089472,
            0.0775,
            0.06281417,
            0.04718583,
            0.0325,
            0.020528,
            0.01271383,
            0.01,
        ]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_inverse_time():
    rates = inverse_time_decay(n_steps=10, initial_value=0.1, decay_rate=0.5)

    true_values = np.array(
        [
            0.1,
            0.09473684,
            0.09,
            0.08571429,
            0.08181818,
            0.07826087,
            0.075,
            0.072,
            0.06923077,
            0.06666667,
        ]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_polynomial():
    rates = polynomial_decay(n_steps=10, initial_value=0.1, end_value=0.001, power=2)

    true_values = np.array(
        [
            0.1,
            0.07922222,
            0.06088889,
            0.045,
            0.03155556,
            0.02055556,
            0.012,
            0.00588889,
            0.00222222,
            0.001,
        ]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_piecewise_constant():
    rates = piecewise_constant_decay(
        n_steps=10, boundaries=[3, 7], values=[0.1, 0.05, 0.01]
    )

    true_values = np.array([0.1, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05, 0.01, 0.01, 0.01])

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_constant():
    rates = constant(n_steps=10, value=0.1)

    true_values = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1])

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_exponential_staircase():
    rates = exponential_decay(
        n_steps=10, initial_value=0.1, decay_rate=0.5, staircase=True
    )

    true_values = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.05])

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_inverse_time_staircase():
    rates = inverse_time_decay(
        n_steps=10, initial_value=0.1, decay_rate=0.5, staircase=True
    )

    true_values = np.array([0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1, 0.06666667])

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_polynomial_cycle():
    rates = polynomial_decay(
        n_steps=10, initial_value=0.1, end_value=0.001, power=2, cycle=True
    )

    true_values = np.array(
        [
            np.nan,
            0.07922222,
            0.06088889,
            0.045,
            0.03155556,
            0.02055556,
            0.012,
            0.00588889,
            0.00222222,
            0.001,
        ]
    )

    assert np.all(np.round(rates[1:], 4) == np.round(true_values[1:], 4))


def test_geometric():
    rates = geometric_decay(
        n_steps=10, initial_value=0.5, decay_rate=0.5, minimum_value=0.01
    )

    true_values = np.array(
        [0.5, 0.5, 0.25, 0.125, 0.0625, 0.03125, 0.015625, 0.01, 0.01, 0.01]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_arithmetic():
    rates = arithmetic_decay(
        n_steps=10, initial_value=0.5, decay_rate=0.5, minimum_value=0.01
    )

    true_values = np.array([0.5, 0.5, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01])

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_time_decay():
    rates = time_decay(n_steps=10, initial_value=0.1, decay_rate=0.1)

    true_values = np.array(
        [
            0.1,
            0.1,
            0.09090909,
            0.07575758,
            0.05827506,
            0.04162504,
            0.02775003,
            0.01734377,
            0.01020222,
            0.0056679,
        ]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))


def test_step_decay():
    rates = step_decay(n_steps=10, initial_value=0.1, decay_value=0.5, decay_every=2)

    true_values = np.array(
        [0.1, 0.1, 0.05, 0.05, 0.025, 0.025, 0.0125, 0.0125, 0.00625, 0.00625]
    )

    assert np.all(np.round(rates, 5) == np.round(true_values, 5))
