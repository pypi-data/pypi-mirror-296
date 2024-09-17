from setuptools import setup
from schedule_kspc import __version__, __author__, __desc__

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


setup(
    name='schedule_kspc',
    version=__version__,
    description=__desc__,
    author='bonkibon',
    author_email=__author__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['schedule_kspc'],
    install_requires=[
        'openpyxl',
        'aiofiles',
        'aiohttp',
    ],
    url='https://github.com/bonkibon-education/schedule-kspc',
    download_url=f"https://github.com/bonkibon-education/schedule-kspc/archive/refs/tags/{__version__}.zip",
    classifiers=[
        "License :: OSI Approved :: GNU Affero General Public License v3",
    ]
)
