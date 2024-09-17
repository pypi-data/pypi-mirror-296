from setuptools import setup, find_packages
import codecs
import os
# 
here = os.path.abspath(os.path.dirname(__file__))
# 
with open(os.path.join(os.path.abspath(os.path.dirname(__file__)),'README.md'), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()\

from pathlib import Path
this_directory = Path(__file__).parent
#long_description = (this_directory / "README.md").read_text()

VERSION = '''0.11'''
DESCRIPTION = '''Sendevent - Android with Cython'''

# Setting up
setup(
    name="cythonsendevent",
    version=VERSION,
    license='MIT',
    url = 'https://github.com/hansalemaos/cythonsendevent',
    author="Johannes Fischer",
    author_email="aulasparticularesdealemaosp@gmail.com",
    description=DESCRIPTION,
long_description = long_description,
long_description_content_type="text/markdown",
    #packages=['Cython', 'exceptdrucker', 'numpy', 'regex', 'setuptools'],
    keywords=['Android', 'Sendevent'],
    classifiers=['Development Status :: 4 - Beta', 'Programming Language :: Python :: 3 :: Only', 'Programming Language :: Python :: 3.10', 'Topic :: Software Development :: Libraries :: Python Modules', 'Topic :: Utilities'],
    install_requires=['Cython', 'exceptdrucker', 'numpy', 'regex', 'setuptools'],
    include_package_data=True
)
#python setup.py sdist bdist_wheel
#twine upload dist/*