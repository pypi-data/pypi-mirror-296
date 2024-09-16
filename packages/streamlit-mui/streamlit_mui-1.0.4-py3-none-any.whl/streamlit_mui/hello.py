"""
This module provides the introduction entry point for streamlit MUI module.

Author: Dilip Thakkar [dilip.thakkar.eng@gmail.com]
"""
from streamlit_mui import (bar_chart, DefaultBarChartConfig, BarData,
                           GroupBarChartConfig, GroupBarData, GroupSeriesData)

import streamlit as st

st.set_page_config(layout="wide")

default_bar_chart_config = DefaultBarChartConfig(data=[
    BarData("Jan", 400),
    BarData("Feb", 100),
    BarData("March", 100),
    BarData("April", 400),
    BarData("May", 100),
    BarData("June", 140),
    BarData("July", -100),
    BarData("August", 100),
    BarData("September", 100),
    BarData("October", 100),
    BarData("November", 80),
    BarData("December", 100),
],
    bar_color='#004b85',
    x_axis_label="Month", y_axis_label="Rain count")

group_bar_chart_config = GroupBarChartConfig(
    x_axis_label="Month", y_axis_label="Score", data=[
        GroupSeriesData("Jan", data=[
            GroupBarData("London", 100),
            GroupBarData("Paris", 40)
        ]),
        GroupSeriesData("Feb", data=[
            GroupBarData("London", 90),
            GroupBarData("Paris", 60),
            GroupBarData("New York", 160)
        ]),
        GroupSeriesData("March", data=[
            GroupBarData("London", 30),
            GroupBarData("Paris", 90)
        ])
    ],
    series=["London", "Paris", "New York"])


cols = st.columns((5, 5))

with cols[0]:
    bar_chart(key="my_bar_chart_key_2", config=group_bar_chart_config)

with cols[1]:
    bar_chart(key="my_bar_chart_key", config=default_bar_chart_config)
