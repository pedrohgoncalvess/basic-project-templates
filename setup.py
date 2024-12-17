from setuptools import setup

setup(
    name="project-generator",
    version="1.0",
    py_modules=["main"],
    entry_points={
        "console_scripts": [
            "npt=main:main"
        ]
    }
)