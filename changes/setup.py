import os

import setuptools


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(PACKAGE_ROOT, 'requirements.txt')) as f:
    REQUIREMENTS = [r.strip() for r in f.readlines()]


setuptools.setup(
    name='changes',
    version='0.0.0',
    description='changes is a utility for retrieving changelogs',
    long_description=README,
    packages=setuptools.find_packages(exclude=('tests',)),
    install_requires=REQUIREMENTS,
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/experiments/blob/master/changes',
    project_urls={
        'Changelog': ('https://github.com/TheKevJames/experiments/blob/master'
                      '/changes/CHANGELOG.md'),
    },
    include_package_data=True,
    license='MIT',
)
