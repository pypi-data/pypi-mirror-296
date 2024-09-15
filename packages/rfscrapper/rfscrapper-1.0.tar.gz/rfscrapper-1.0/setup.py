from setuptools import setup, find_packages


with open("README.md") as fp:
    long_description = fp.read()

setup(
    name="rfscrapper",
    version="1.0",
    description="A simple web scrapper tool wich downloads podcasts from radiofrance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Cosmow22/radio-france-podcasts-scrapper",
    author="Cosmow22",
    author_email="cosmow543@gmail.com",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "rfscrapper=rfscrapper.main:cli",
        ],
    },
    python_requires='>=3.6',
)
