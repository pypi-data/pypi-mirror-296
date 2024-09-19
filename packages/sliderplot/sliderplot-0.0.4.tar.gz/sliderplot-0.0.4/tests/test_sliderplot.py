import pytest

from sliderplot import sliderplot
import numpy as np


def test_minimal_example():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return x, y

    sliderplot(f, params_bounds=((0, 1),))


def test_multiple_lines():
    def f(amplitude=1, frequency=np.pi, phase=np.pi / 2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return (x, y), (2 * x, 2 * y)

    sliderplot(f)


def test_multiple_plots():
    def f(amplitude=2, frequency=2, phase=2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        return ((x, y),), ((x, 2 * y), (x, x + y))

    sliderplot(f)


def test_lot_of_lines():
    def f(amplitude=2, frequency=2, phase=2):
        x = np.linspace(0, 10, 1000)
        y = amplitude * np.sin(frequency * x + phase)
        multi_lines = []
        for i in range(20):
            multi_lines.append((x, i * y))
        return ((x, y),), multi_lines

    sliderplot(f)
