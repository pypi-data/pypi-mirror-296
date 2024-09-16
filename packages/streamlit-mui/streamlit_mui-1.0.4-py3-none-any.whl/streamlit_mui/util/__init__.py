"""
This module provides utility functions.

Author: Dilip Thakkar [dilip.thakkar.eng@gmail.com]
"""
from typing import Callable
import streamlit as st


def update_kw(kw: dict, **kwargs):
    """
    Updates a given dictionary `kw` with additional keyword arguments and removes specific keys.

    Args:
        kw (dict): The original dictionary to be updated.
        **kwargs: Additional keyword arguments to update the dictionary `kw`.

    Returns:
        dict: The updated dictionary with the specified keys removed.
    """
    r = kw.copy()
    r.update(**kwargs)
    delete_keys = ['key', 'on_change', 'args', 'kwargs', "on_click"]
    for k in delete_keys:
        if k in r.keys():
            del r[k]
    return r


def handle_click_events(key: str, on_click: Callable = None):
    value = st.session_state.get(key, None)
    prev_modified_key = key + "_prev"
    prev_value = st.session_state.get(prev_modified_key, None)

    if value and (not prev_value or prev_value["id"] != value["id"]):
        if on_click:
            on_click()

        st.session_state[prev_modified_key] = value
