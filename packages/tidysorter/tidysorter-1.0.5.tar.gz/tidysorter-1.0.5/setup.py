import re
from pathlib import Path
from setuptools import setup, find_packages

def get_version(package):
    initfile = Path(package, "tidysorter.py").read_text()
    return re.search("__version__ = ['\"]([^'\"]+)['\"]", initfile)[1]

setup(
    name='tidysorter',
    version=get_version("tidysorter"),
    author='Arnaud Le Floch',
    author_email='a.lefloch2491@gmail.com',
    description='A tool to organize files in a directory',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ale-floc/tidysorter',
    packages=find_packages(),
    entry_points={'console_scripts': ['tidysorter=tidysorter.tidysorter:main']},
    install_requires=[]
)