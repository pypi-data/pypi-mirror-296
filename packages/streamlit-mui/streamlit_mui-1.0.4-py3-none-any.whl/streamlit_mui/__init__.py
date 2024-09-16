from streamlit_mui.widgets import *
import os
import subprocess


def hello():
    """
    This function provides an entry point for the introduction of our module
    """
    script_path = os.path.abspath(__file__)

    directory_path = os.path.dirname(script_path)

    hello_file_path = os.path.join(directory_path, "hello.py")

    subprocess.run(["streamlit", "run", hello_file_path])
