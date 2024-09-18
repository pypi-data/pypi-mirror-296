from setuptools import setup, find_packages

setup(
    name='pylogs_DIGITAL_MARKEMATICS',
    version='1.0.3',
    packages=find_packages(),
    install_requires=[
        "psycopg2",
        "configparser",
    ],
    entry_points={
        'console_scripts': [],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
