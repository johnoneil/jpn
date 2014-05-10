# vim: set ts=2 expandtab:
from setuptools import setup

#version 0.1: Initial version

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='jpn',
  version='0.1',
  description='Japanese support tools.',
  long_description = readme(),
	classifiers=[
    'Development Status :: 3 - Alpha',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Natural Language :: Japanese',
  ],
  keywords = 'Japanese transliteration hiragana katakana romaji deinflection verbs',
  url='https://github.com/johnoneil/jpn',
  author='John O\'Neil',
  author_email='oneil.john@gmail.com',
  license='MIT',
  packages=[
    'jpn',
  ],
  install_requires=[
    'argparse',
  ],
  package_data = {
    '': ['*.gz',],
    'weeabot' : ['*',],
  },
  entry_points = {
    'console_scripts': [
      'jpn-transliterate=jpn.transliterate:main',
			'jpn-deinflect=jpn.deinflect:main',
      'jpn-edict=jpn.edict:main',
    ],
  },
  zip_safe=True)
