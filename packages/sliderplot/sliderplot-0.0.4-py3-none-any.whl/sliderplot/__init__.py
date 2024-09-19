import inspect
from inspect import signature
from typing import Callable

import panel as pn

from sliderplot.sliderplot import _BOTTOM_PADDING, _SLIDER_HEIGHT, _get_lines, \
    _create_bokeh_plot

_N_POINTS_PER_SLIDER = 1000

def sliderplot(f: Callable, params_bounds=()):
    """
    Create an interactive plot with sliders to explore the outputs of the function f for different inputs.
    :param f: Function to explore.
    :param params_bounds: Sequence of (val_min, val_max) bounds for each parameter of the function f.
    :return: fig and axs (Axes object if there is one subplot, and list of Axes if there are multiple subplots).
    """
    # Get init parameters
    params = signature(f).parameters
    init_params = [param.default if param.default is not inspect.Parameter.empty else 1 for param in
                   params.values()]
    outputs = f(*init_params)

    pn.extension(design="material")

    # Create sliders
    sliders = []
    for i, param in enumerate(params.keys()):
        if i < len(params_bounds):
            val_min, val_max = params_bounds[i]
        else:
            val_min, val_max = 0, 20
        slider = pn.widgets.EditableFloatSlider(value=init_params[i], start=val_min, end=val_max, name=param,
                                                step=(val_max - val_min) / _N_POINTS_PER_SLIDER)
        sliders.append(slider)

    fig, lines_source, plot_mode = _create_bokeh_plot(outputs)

    def simulate(*args):
        try:
            new_outputs = f(*args)
        except ZeroDivisionError:
            return
        for line, (x, y) in zip(lines_source, _get_lines(new_outputs, plot_mode)):
            line.data = dict(x=x, y=y)
        return fig

    curves = pn.bind(simulate, *sliders)

    plot = pn.pane.Bokeh(curves, sizing_mode="stretch_both")

    # Dirty trick to fix bug that make the plot empty when init with multiple plots
    sliders[0].value = init_params[0] + 0.0000000001
    sliders[0].value = init_params[0]

    server = pn.template.MaterialTemplate(
        title="Sliderplot",
        sidebar=sliders,
        main=plot,
    ).show()
    # Stop server on close
    server.stop()
