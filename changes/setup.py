import os

import setuptools


PACKAGE_ROOT = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(PACKAGE_ROOT, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(PACKAGE_ROOT, 'requirements.txt')) as f:
    REQUIREMENTS = [r.strip() for r in f.readlines()]


setuptools.setup(
    name='getchanges',
    version='0.0.0',
    description='getchanges is a utility for retrieving changelogs',
    long_description=README,
    packages=setuptools.find_packages(exclude=('tests',)),
    python_requires='>= 3.5',
    install_requires=REQUIREMENTS,
    author='Kevin James',
    author_email='KevinJames@thekev.in',
    url='https://github.com/TheKevJames/experiments/blob/master/getchanges',
    project_urls={
        'Changelog': ('https://github.com/TheKevJames/experiments/blob/master'
                      '/getchanges/CHANGELOG.md'),
    },
    include_package_data=True,
    platforms='Posix; MacOS X; Windows',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points={
        'console_scripts': [
            'changes = getchanges.__main__:main',
        ],
    },
)
