# Welcome to Streamlit MUI

<img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" alt="Streamlit logo" style="margin-top:50px"></img>


This Python library provides a flexible way to integrate Material UI components in your streamlit application. As of now this includes single bar and grouped bar charts. In near future a lot of MUI components will be provided by this library.

## Installation

Open a terminal and run

```cmd
$ pip install streamlit_mui
$ streamlit_mui_hello
```

## Usage

### Creating a Single Series Bar Chart

To create a bar chart, use the DefaultBarChartConfig class to define the chart's configuration, then pass it to the bar_chart function to render the chart.

```python
from streamlit_mui import bar_chart, DefaultBarChartConfig, BarData

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

bar_chart(key="bar_chart_unique_key", config=default_bar_chart_config)
```

## Usage

### Creating a Grouped Series Bar Chart

For a grouped bar chart, use the GroupBarChartConfig class. Define the data for each group using GroupSeriesData and GroupBarData.

```python
from streamlit_mui import bar_chart, GroupBarChartConfig, GroupBarData, GroupSeriesData

group_bar_chart_config = GroupBarChartConfig(
    x_axis_label="Month",
    y_axis_label="Score",
    data=[
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

bar_chart(key="bar_chart_unique_key", config=group_bar_chart_config)
```

![](https://github.com/user-attachments/assets/9cb2ad3c-8f9a-4f86-a3d6-8440cda87ebb)

## Author
- Dilip Thakkar [dilip.thakkar.eng@gmail.com]
- LinkedIn [https://www.linkedin.com/in/dilip-thakkar-465898194/]
