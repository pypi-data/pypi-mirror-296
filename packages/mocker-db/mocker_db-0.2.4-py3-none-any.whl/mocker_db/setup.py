from setuptools import setup

import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))
path_to_readme = os.path.join(here, "README.md")

long_description = """# Mocker db

MockerDB is a python module that contains mock vector database like solution built around
python dictionary data type. It contains methods necessary to interact with this 'database',
embed, search and persist.

"""

if os.path.exists(path_to_readme):
  with codecs.open(path_to_readme, encoding="utf-8") as fh:
      long_description += fh.read()

setup(
    name="mocker_db",
    packages=["mocker_db"],
    install_requires=['gridlooper==0.0.1', 'attrs==23.2.0', 'numpy==1.26.0', 'dill==0.3.7', 'httpx', 'requests'],
    classifiers=['Development Status :: 3 - Alpha', 'Intended Audience :: Developers', 'Intended Audience :: Science/Research', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.9', 'Programming Language :: Python :: 3.10', 'Programming Language :: Python :: 3.11', 'License :: OSI Approved :: MIT License', 'Topic :: Scientific/Engineering'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="Kyrylo Mordan",
    author_email="parachute.repo@gmail.com",
    description="A mock handler for simulating a vector database.",
    license="mit",
    keywords="['aa-paa-tool']",
    version="0.2.4",
    extras_require = {'sentence-transformers': ['sentence-transformers==2.2.2'], 'hnswlib': ['hnswlib==0.8.0'], 'all': ['sentence-transformers==2.2.2', 'hnswlib==0.8.0']},

)
