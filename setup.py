"""Our setup script."""

import glob
from setuptools import setup

setup(
    name="gpex",
    description="Experiments with generalized pruning",
    packages=["gpex"],
    package_data={"gpex": ["data/*"]},
    scripts=glob.glob("gpex/scripts/*.sh"),
    entry_points={"console_scripts": ["gpex=gpex.cli:cli"]},
    install_requires=[
        "click-config-file",
        "csvkit",
        "dendropy",
        "plotnine==0.6.0",
        "pylint",
        "pytest",
    ],
)
