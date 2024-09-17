import setuptools
from distutils.core import setup

setup(
    name="utils-cli_sjain02",
    version="0.3.0",
    description="Utility functions",
    author="Saurabh Jain",
    author_email="jpr.saurabh@gmail.com",
    packages=["sj_util","sj_util/helpers"],
    entry_points={
        "console_scripts":[
            "clarity-cli=sj_util.clarity_cli:cli_entry_point",
            "con-cli=sj_util.conall_cli:cli_entry_point",
            "marker-cli=sj_util.marker_cli:cli_entry_point",
            ],
    },
    install_requires=[
        "urltitle"
    ],
    python_requires='>=3.6'
)