from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.0.1'
DESCRIPTION = 'Provides HTML & CSS information based on keyword arguments and filepaths, including styling, unused classes, and other relevant data.'

# Setting up
setup(
    name="stylemapper",
    version=VERSION,
    
    author="Josh Hofer",
    author_email="<josh@securesap.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['beautifulsoup4', 'tabulate'],
    keywords=['python', 'css', 'html', 'front-end', 'remove unused css'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Natural Language :: English",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    entry_points={
      'console_scripts': [
        'stylemapper=stylemapper.stylemapper:main',
      ],
    },
    project_urls={
        "Source": "https://github.com/JoshHofer01/StyleMapper",
    }
)