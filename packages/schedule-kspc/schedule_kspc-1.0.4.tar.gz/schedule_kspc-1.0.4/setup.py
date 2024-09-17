from setuptools import setup
from schedule_kspc import __version__, __author__, __desc__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='schedule_kspc',
    version=f'{__version__}.4',
    description=__desc__,
    author='bonkibon',
    author_email=__author__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=["schedule_kspc"],
    install_requires=[
        'requests',
        'aiofiles',
        'aiohttp',
        'numpy',
        'openpyxl'
    ],
    url='https://github.com/bonkibon-education/schedule-kspc',
    download_url=f"https://github.com/bonkibon-education/schedule-kspc/archive/refs/tags/v{__version__}-beta.zip",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ]
)