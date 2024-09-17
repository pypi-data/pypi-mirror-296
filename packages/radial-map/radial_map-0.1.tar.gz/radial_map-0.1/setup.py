from setuptools import setup, find_packages

setup(
    name="radial_map",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "matplotlib",
        "numpy",
    ],
    description="Package for creating polar-based radial maps in MPL",
    author="Matt",
    author_email="matthewkotzbauer@college.harvard.edu",
    url="https://github.com/MattKotzbauer/radial-map",
)

