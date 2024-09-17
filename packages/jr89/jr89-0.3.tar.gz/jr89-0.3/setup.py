from setuptools import setup,find_packages

setup(
    name="jr89",
    version="0.3",
    packages=find_packages(),
    install_requires = [],
    entry_points = {
        "console_scripts" : [
            "jr89 = jr89 : jr89_welcome",
        ]
    }
)