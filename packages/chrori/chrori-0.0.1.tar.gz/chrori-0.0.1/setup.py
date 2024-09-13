#!/usr/bin/env python
from setuptools import setup, find_packages # type: ignore
from chrori.__init__ import __version__

setup(name='chrori',
      version=__version__,
      description='A tool to visualize the origins of chromosome segments whose lines developed from multiple crosses.',
      author='Koki Chigira',
      author_email='kyoujin2009kutar@gmail.com',
      url='https://github.com/KChigira/chrori/',
      license='MIT',
      packages=find_packages(),
      install_requires=[
        'pandas',
        'matplotlib',
      ],
      entry_points={'console_scripts': [
            'chrori_mkvcf = chrori.mkvcf:main',
            'chrori_select = chrori.selectvariants:main',
            'chrori_visual = chrori.visualize:main',
            ]
      }
    )
