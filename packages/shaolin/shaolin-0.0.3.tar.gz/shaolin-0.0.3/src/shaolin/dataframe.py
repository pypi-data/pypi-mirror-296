from collections.abc import Callable
import functools

from bokeh.models import HoverTool
import holoviews as hv
import numpy as np
import pandas as pd
import panel as pn
import param

from shaolin.utils import find_closest_point
from shaolin.dimension_mapper import (
    AlphaDim,
    ColorDim,
    Dimensions,
    is_string_column,
    organize_widgets,
    SizeDim,
    widget_priority,
)


def select_index(xy_columns: list[str] | None = None, df: pd.DataFrame | None = None) -> Callable:
    """Decorator that transforms a function by finding the index of the closest point.

    This decorator takes the `xy_columns` and an optional `df` as arguments and returns a \
    new function that takes `ix` and `df` as arguments. Inside the decorator, \
    it calls the original function with the index of the closest point and the dataframe.

    If `df` is provided when using the decorator, it will be used as the default dataframe \
    for the decorated function.

    Args:
        xy_columns (List[str], optional): List of column names to be used for x and y
                                          coordinates. Defaults to ["x", "y"].
        df (pd.DataFrame, optional): Default dataframe to be used in the decorated function.
                                      If not provided, the dataframe must be passed as an argument
                                      when calling the decorated function. Defaults to None.

    Returns:
        Callable: The new function that takes `ix` and `df` as arguments.

    """
    if xy_columns is None:
        xy_columns = ["x", "y"]

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(x: float, y: float, df_: pd.DataFrame = None) -> Callable:
            nonlocal df
            if df_ is not None:
                df = df_
            if df is None:
                msg = (
                    "A dataframe must be provided when calling the "
                    "decorated function, or when using the decorator."
                )
                raise ValueError(msg)
            points = df[xy_columns].values
            ix = find_closest_point(points, x, y)
            return func(ix, df)

        return wrapper

    return decorator


def view_plot(
    self,
    dim_x: str = "x",
    dim_y: str = "y",
    ignore_cols: tuple[str] | None = ("states",),
    **kwargs,
):
    df = self.df
    if ignore_cols:
        df = df.drop(columns=[c for c in ignore_cols if c in df.columns])
    hover_cols = [c for c in df.columns if not is_string_column(df, c)]
    tooltips = [("Index", "$index")] + [
        (n.capitalize().replace("_", " "), f"@{n}") for n in hover_cols
    ]
    hover = HoverTool(tooltips=tooltips)
    return hv.Scatter(df, kdims=[dim_x], vdims=[dim_y, *hover_cols]).opts(
        width=self.width.value,
        height=self.height.value,
        title="",
        framewise=True,
        colorbar=True,
        tools=[hover],
        **kwargs,
    )


class InteractiveDataFrame(param.Parameterized):
    def __init__(
        self,
        df: pd.DataFrame,
        ignore_cols: tuple[str] | None = None,
        n_cols=3,
        default_x_col: str | None = None,
        default_y_col: str | None = None,
    ):
        self.n_cols = n_cols
        super().__init__()
        self.df = df

        if ignore_cols is None:
            ignore_cols = tuple(c for c in df.columns if is_string_column(self.df, c))
        self.ignore_cols = ignore_cols
        self.width = pn.widgets.IntSlider(name="width", start=400, end=2000, value=1000)
        self.height = pn.widgets.IntSlider(name="height", start=400, end=2000, value=600)
        self.df_dims = Dimensions(
            self.df,
            self.n_cols,
            size=SizeDim,
            color=ColorDim,
            alpha=AlphaDim,
        )
        valid_columns = self.df_dims.dimensions["size"].valid_cols
        default_x_col = default_x_col or valid_columns[0]
        default_y_col = default_y_col or valid_columns[1]
        self.sel_x = pn.widgets.Select(name="x", options=valid_columns, value=default_x_col)
        self.sel_y = pn.widgets.Select(name="y", options=valid_columns, value=default_y_col)
        streams = self.df_dims.streams
        streams["dim_x"] = self.sel_x.param.value
        streams["dim_y"] = self.sel_y.param.value
        self.dmap = hv.DynamicMap(functools.partial(view_plot, self=self), streams=streams)
        self.tap_stream = hv.streams.Tap(source=self.dmap, x=np.nan, y=np.nan)

    def bind_to_stream(self, function: Callable):
        return pn.bind(function, x=self.tap_stream.param.x, y=self.tap_stream.param.y)

    def bind_tap(self, func: Callable, df: pd.DataFrame | None = None) -> Callable:
        """Bind a function to the tap event of the plot."""

        @functools.wraps(func)
        def wrapper(x: float, y: float, df_: pd.DataFrame = None) -> Callable:
            nonlocal df
            if df_ is not None:
                df = df_
            if df is None:
                df = self.df
            xy_cols = [self.sel_x.value, self.sel_y.value]
            points = df[xy_cols].values.astype(float)
            ix = find_closest_point(points, x, y)
            return func(ix, df)

        return self.bind_to_stream(wrapper)

    @param.depends("sel_x.value", "sel_y.value")
    def update_lims(self):
        self.dmap = self.dmap.redim.range(
            x=(self.df[self.sel_x.value].min(), self.df[self.sel_x.value].max()),
            y=(self.df[self.sel_y.value].min(), self.df[self.sel_y.value].max()),
        )

    def layout(self):
        all_dims = self.df_dims.dimensions
        dimensions = dict(sorted(all_dims.items(), key=widget_priority))
        widgets = [dimension.panel() for dimension in dimensions.values()]
        return pn.Column(
            organize_widgets(widgets, self.n_cols, sizing_mode="stretch_width"),
            pn.Row(pn.Column(self.sel_x, self.sel_y), pn.Column(self.height, self.width)),
        )

    def view(self):
        hv_panel = pn.pane.HoloViews(self.dmap)
        self.height.link(hv_panel[0], value="height")
        self.width.link(hv_panel[0], value="width")
        return pn.Row(hv_panel, self.update_lims)

    def __panel__(self):
        return pn.Column(self.layout, self.view)
