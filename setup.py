import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

REQUIREMENTS = [
    # Add your list of production dependencies here, eg:
    # 'requests == 2.*',
]

DEV_REQUIREMENTS = [
    'black == 22.*',
    'build == 0.7.*',
    'coveralls == 3.*',
    'flake8 == 4.*',
    'isort == 5.*',
    'mypy == 0.942',
    'pytest == 7.*',
    'pytest-cov == 3.*',
    'twine == 4.*',
]

setuptools.setup(
    name='inverted_index',
    version='0.1.0',
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/xmadera/inverted_index',
    author='xmadera',
    license='MIT',
    packages=setuptools.find_packages(
        exclude=[
            'examples',
            'test',
        ]
    ),
    package_data={
        'inverted_index': [
            'py.typed',
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    extras_require={
        'dev': DEV_REQUIREMENTS,
    },
    entry_points={
        'console_scripts': [
            'PROJECT_NAME_URL=inverted_index.my_module:main',
        ]
    },
    python_requires='>=3.7, <4',
)
