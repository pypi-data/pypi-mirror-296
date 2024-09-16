"""
This module provides utility functions to create bar chart in streamlit

Author: Dilip Thakkar [dilip.thakkar.eng@gmail.com]
"""

from streamlit_mui.component import react_component
from typing import List
from streamlit_mui.util import update_kw


class BarChartConfig:
    """
    Represents the base configuration object for creating bar charts.

    Attributes:
        width (int, optional): The width of the bar chart.
        height (int, optional): The height of the bar chart.
        x_axis_label (str, optional): The label for the x-axis.
        y_axis_label (str, optional): The label for the y-axis.
        variant (str, optional): The variant of the bar chart. Default is "default".
    """

    def __init__(self, width: int = None, height: int = None, x_axis_label: str = None, y_axis_label: str = None, variant: str = "default") -> None:
        self.width = width
        self.height = height
        self.x_axis_label = x_axis_label
        self.y_axis_label = y_axis_label
        self.variant = variant

    def to_dict(self):
        """
        Converts the configuration object to a dictionary.

        Returns:
            dict: A dictionary representation of the configurations.
        """
        return {"width": self.width,
                "height": self.height,
                "xAxisLabel": self.x_axis_label,
                "yAxisLabel": self.y_axis_label,
                "variant": self.variant}


class BarData:
    """
    Represents the bar of a default bar chart.

    Each bar is defined by an x_label, which will be used as the label for the x-axis, and a value, 
    which will be used to represent the height of the bar.

    Attributes:
        x_label (str): The label for the x-axis.
        value (int): The value representing the height of the bar.
    """

    def __init__(self, x_label: str, value: int) -> None:
        self.x_label = x_label
        self.value = value

    def to_dict(self):
        """
        Converts the BarData object to a dictionary.

        Returns:
            dict: A dictionary representation of the bar data.
        """
        return {"xLabel": self.x_label, "value": self.value}


class DefaultBarChartConfig(BarChartConfig):
    """
    Represents the configuration object for creating a default bar chart.

    Inherits from BarChartConfig and adds additional attributes specific to a default bar chart, such as data and bar color.

    Attributes:
        width (int, optional): The width of the bar chart.
        height (int, optional): The height of the bar chart.
        x_axis_label (str, optional): The label for the x-axis.
        y_axis_label (str, optional): The label for the y-axis.
        data (List[BarData]): The data for the bars in the chart.
        bar_color (str, optional): The color of the bars in the chart.
    """

    def __init__(self, width: int = None, height: int = None,
                 x_axis_label: str = None,
                 y_axis_label: str = None,
                 data: List[BarData] = None,
                 bar_color: str = None) -> None:
        super().__init__(width, height, x_axis_label, y_axis_label)
        self.data = data or []
        self.bar_color = bar_color

    def to_dict(self):
        return {**super().to_dict(),
                "data": [bar_data.to_dict() for bar_data in self.data],
                "barColor": self.bar_color}


class GroupBarData:
    """
    Represents a single data point in a grouped bar chart.

    Attributes:
        series_name (str): The name of the series this data point belongs to.
        value (int): The value of this data point.
    """

    def __init__(self, series_name: str, value: int) -> None:
        self.series_name = series_name
        self.value = value


class GroupSeriesData:
    """
    Represents a group of data points in a grouped bar chart.

    Each group contains multiple data points, each represented by a GroupBarData object.

    Attributes:
        group_name (str): The name of the group.
        data (List[GroupBarData]): A list of GroupBarData objects representing the data points in this group.
    """

    def __init__(self, group_name, data: List[GroupBarData] = None) -> None:
        self.group_name = group_name
        self.data: List[GroupBarData] = data or []

    def to_dict(self):
        return {
            "groupName": self.group_name,
            **{grp_bar_data.series_name: grp_bar_data.value for grp_bar_data in self.data}
        }


class GroupBarChartConfig(BarChartConfig):
    """
    Represents the configuration object for creating a grouped bar chart.

    Inherits from BarChartConfig and adds additional attributes specific to a grouped bar chart,
    such as series data and the series names.

    Attributes:
        width (int, optional): The width of the bar chart.
        height (int, optional): The height of the bar chart.
        x_axis_label (str, optional): The label for the x-axis.
        y_axis_label (str, optional): The label for the y-axis.
        data (List[GroupSeriesData]): The data for the grouped bars in the chart.
        series (List[str]): A list of series names for the grouped bars.
    """

    def __init__(self, width: int = None,
                 height: int = None,
                 x_axis_label: str = None,
                 y_axis_label: str = None,
                 data: List[GroupSeriesData] = None,
                 series: List[str] = None) -> None:
        super().__init__(width, height, x_axis_label, y_axis_label, "group")
        self.data: List[GroupBarData] = data or []
        self.series: List[str] = series or []

    def to_dict(self):
        return {**super().to_dict(),
                "data": [data.to_dict() for data in self.data], "series": self.series}


def bar_chart(key: str, config: BarChartConfig):
    """
    Renders a bar chart using the given configuration and key.

    This function prepares the configuration by converting it to a dictionary, updates the keyword arguments,
    and then calls the React component to render the bar chart.

    Args:
        key (str): The unique key identifier for the bar chart.
        config (BarChartConfig): The configuration object for the bar chart.
    """

    kw = update_kw(locals(), config=config.to_dict())

    react_component(type="bar_chart", kw=kw, key=key)
