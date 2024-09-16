#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    "faker",
    "Rich",
    "PyYAML",
]

test_requirements = []

setup(
    author="Jaideep Sundaram",
    author_email='jai.python3@gmail.com',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="Collection of Python modules for masking PHI in delimited files and Excel worksheets.",
    entry_points={
        'console_scripts': [
            'mask-file=phi_masker_utils.mask_file:main',
        ],
    },
    install_requires=requirements,
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='phi_masker_utils',
    name='phi_masker_utils',
    packages=find_packages(
        include=[
            'phi_masker_utils',
            'phi_masker_utils/*',
        ]
    ),
    package_data={
        "phi_masker_utils": [
            "conf/config.yaml",
        ]
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/jai-python3/phi-masker-utils',
    version='0.1.0',
    zip_safe=False,
)
