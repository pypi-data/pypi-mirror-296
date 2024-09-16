"""
This module provides a react component that can be used in streamlit applications.

Author: Dilip Thakkar [dilip.thakkar.eng@gmail.com]
"""
import os
from typing import Any, Callable

import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "react_component",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "react_component", path=build_dir)


def react_component(type: str, kw, key: str = None, on_change: Callable = None) -> Any:

    component_value = _component_func(
        type=type,
        kw=kw,
        key=key,
        on_change=on_change
    )
    return component_value
