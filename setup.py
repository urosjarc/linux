#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.md') as readme_file:
    readme = readme_file.read()

requirements = [
	'sh'
]

test_requirements = [
]

setup(
    name='mylinux',
    version='0.0.1',
    description="Linux post installation helper and manager.",
    long_description=readme,
    author="Uroš Jarc",
    author_email='jar.fmf@gmail.com',
    url='https://github.com/urosjarc/mylinux',
    packages=[
        'mylinux',
    ],
    package_dir={'mylinux':
                 'mylinux'},
    entry_points={
        'console_scripts': [
            'mylinux=mylinux.cli:main'
        ]
    },
    include_package_data=False,
    install_requires=requirements,
    license="MIT license",
    zip_safe=True,
    keywords='mylinux',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
