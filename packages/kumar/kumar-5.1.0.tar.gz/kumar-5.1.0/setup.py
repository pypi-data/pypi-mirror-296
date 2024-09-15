from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '5.1.0'
DESCRIPTION = '`kumar` is a Python package that provides two high-level features.'
LONG_DESCRIPTION = 'This is Ai Transformer of easily ways.'

# Setting up
setup(
    name="kumar",
    version=VERSION,
    author="manishkumar60708090@gmail.com",
    author_email="<manishkumar60708090@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=['torch', 'tqdm', 'datasets', 'tokenizers', 'tensorboard', 'pathlib', 'pillow'],
    keywords=['python', 'transformer', 'chat-GPT Transformer'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)