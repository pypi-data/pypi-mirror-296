from pathlib import Path

from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="dgtl_logging",
    version="0.2.0",
    description="DGTL Health BV NEN7513 compliant logging objects ",
    author="Olivier Witteman",
    license="MIT",
    packages=["dgtl_logging"],
    install_requires=['uuid'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
    ]
)
