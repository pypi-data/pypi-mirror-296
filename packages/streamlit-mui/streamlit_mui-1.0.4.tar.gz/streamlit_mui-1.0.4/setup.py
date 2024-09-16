"""
This module provides setup configurations to create a build that can be uploaded on pypi server.

Author: Dilip Thakkar [dilip.thakkar.eng@gmail.com]
"""
import setuptools

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setuptools.setup(
    name='streamlit_mui',
    version='1.0.4',
    author="Dilip Thakkar",
    author_email="dilip.thakkar.eng@gmail.com",
    description='Streamlit module which provides implementation of various Material UI components',
    long_description=long_description,
    long_description_content_type='text/markdown',
    py_module=['streamlit_mui'],
    packages=setuptools.find_packages(exclude=('venv')),
    package_data={'streamlit_mui': [
        'component/frontend/build/**']},
    python_requires='>=3.9.0',
    install_requires=['streamlit >= 1.36.0'],
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'streamlit_mui_hello=streamlit_mui:hello',
        ],
    },
)
