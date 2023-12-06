from setuptools import setup

setup(
    name="talent",
    version="0.1.0",
    py_modules=["talent.cli"],
    install_requires=[
        "evesso",
        "pandas",
        "python-dotenv",
        "requests-futures",
    ],
    entry_points={
        "console_scripts": [
            "talent = talent.main:cli",
        ],
    },
)
