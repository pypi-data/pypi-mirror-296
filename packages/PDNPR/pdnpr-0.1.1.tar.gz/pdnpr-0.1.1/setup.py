from setuptools import setup, find_packages
import codecs
import os

# these things are needed for the README.md show on pypi (if you dont need delete it)
here = os.path.abspath(os.path.dirname(__file__))
DESCRIPTION = 'Tool to find allosteric route based on MD files'
with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()
setup(
    name='PDNPR',
    version='0.1.1',
    packages=find_packages(),
    author="Spencer Wang",
    author_email="jrwangspencer@stu.suda.edu.cn",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    install_requires=[
        'networkx',
        'tqdm',
        'mdtraj',
        'contourpy==1.2.1',
        'cycler==0.12.1',
        'fonttools==4.51.0',
        'kiwisolver==1.4.5',
        'matplotlib==3.9.0',
        'pillow==10.3.0',
    ],
    extras_require={
        'tk': [],  # Optional tkinter requirement (usually included with Python)
    },
    keywords=['Python', 'Protein', 'allosteric', 'Network', 'Shortest route', 'windows', 'mac', 'linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires='>=3.9',  # Set according to your project's compatibility
)