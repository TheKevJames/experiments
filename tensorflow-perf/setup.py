import os

import setuptools


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PACKAGE_ROOT, 'requirements.txt')) as f:
    REQUIREMENTS = [r.strip() for r in f.readlines()]


setuptools.setup(
    name='g2p',
    version='1.0.0',
    packages=['g2p'],
    install_requires=REQUIREMENTS,
    python_requires='>= 3.6',
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/thekevjames/experiments',
    include_package_data=True,
    zip_safe=True
)
