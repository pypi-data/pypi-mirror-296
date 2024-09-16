
from typing import Callable
from streamlit_mui.component import react_component
from streamlit_mui.util import update_kw, handle_click_events
from enum import Enum

class Size(Enum):
    SMALL = "xs"
    MEDIUM = "sm"
    LARGE = "lg"


def icon_button(key: str,
                icon: str,
                size: Size = Size.SMALL,
                on_click: Callable = None,
                color: str = "black",
                background_color: str = "lightgrey"):

    kw = update_kw(locals(), size=size.value)

    modified_key = key + "icon_button"

    react_component(type="icon_button", kw=kw,
                    key=modified_key, on_change=lambda: handle_click_events(modified_key, on_click))
