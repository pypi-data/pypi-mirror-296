import enum
import itertools

import numpy as np
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import d3

_SLIDER_HEIGHT = 0.05
_BOTTOM_PADDING = (0.03, 0.1)


class _PlotMode(enum.Enum):
    LINE_X = 0
    LINE_XY = 1
    MULTI_LINE = 2
    MULTI_PLOT = 3


def _get_plot_mode(output_data) -> _PlotMode:
    plot_mode_map = {1: _PlotMode.LINE_X, 2: _PlotMode.LINE_XY, 3: _PlotMode.MULTI_LINE, 4: _PlotMode.MULTI_PLOT}
    depth = _compute_depth(output_data)
    if depth in plot_mode_map.keys():
        return plot_mode_map[depth]
    else:
        raise Exception("Failed to transform the output data of the function into plots. "
                        "Please look at the documentation for correct data formatting.")


def _compute_depth(data) -> int:
    # TODO: check depth of all elements
    depth = 0
    current_element = data
    while True:
        try:
            current_element = current_element[0]
            depth += 1
        except IndexError:
            break
    return depth


def _create_bokeh_plot(outputs):
    lines_source = []
    plot_mode = _get_plot_mode(outputs)
    if plot_mode is _PlotMode.MULTI_PLOT:
        figs = []
        for subplot_data in outputs:
            sub_fig = None
            colors = itertools.cycle(d3["Category20"][19])
            for x, y in subplot_data:
                sub_fig, line_source = _create_bokeh_figure(x, y, colors, fig=sub_fig)
                lines_source.append(line_source)
            figs.append(sub_fig)
        fig = column(*figs)
    else:
        if plot_mode is _PlotMode.MULTI_LINE:
            fig = None
            colors = itertools.cycle(d3["Category20"][19])
            for x, y in outputs:
                fig, line_source = _create_bokeh_figure(x, y, fig=fig, colors=colors)
                lines_source.append(line_source)
        elif plot_mode is _PlotMode.LINE_XY:
            fig, line_source = _create_bokeh_figure(outputs[0], outputs[1])
            lines_source.append(line_source)
        elif plot_mode is _PlotMode.LINE_X:
            x = np.arange(len(outputs))
            fig, line_source = _create_bokeh_figure(x, outputs)
            lines_source.append(line_source)
        else:
            raise Exception(f"This mode is not supported: {plot_mode}")
    return fig, lines_source, plot_mode


TOOLTIPS = [
    ("x", "$x"),
    ("y", "$y")
]


def _create_bokeh_figure(x, y, colors=None, fig=None):
    line_source = ColumnDataSource(data=dict(x=x, y=y))
    if fig is None:
        fig = figure(tools="pan,reset,save, box_zoom,wheel_zoom", sizing_mode="stretch_both")
        fig.add_tools(HoverTool(mode="vline", tooltips=TOOLTIPS))
    if colors is not None:
        fig.line('x', 'y', source=line_source, line_width=3, color=next(colors))
        _ = next(colors)  # Trick to use last the uneven colors of the palette
    else:
        fig.line('x', 'y', source=line_source, line_width=3)
    return fig, line_source


def _get_lines(outputs, plot_mode: _PlotMode):
    if plot_mode is _PlotMode.MULTI_LINE:
        return outputs
    elif plot_mode is _PlotMode.LINE_XY:
        return ((outputs[0], outputs[1]),)
    elif plot_mode is _PlotMode.LINE_X:
        x = np.arange(len(outputs))
        return ((x, outputs),)
    elif plot_mode is _PlotMode.MULTI_PLOT:
        return np.concatenate((*outputs,))
    else:
        raise Exception("Invalid plot_mode argument.")
