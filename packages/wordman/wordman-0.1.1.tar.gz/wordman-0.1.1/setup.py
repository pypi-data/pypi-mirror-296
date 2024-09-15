from setuptools import setup, find_packages

setup(
    name='wordman',
    version='0.1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wordman=wordman:main',
        ],
    },
    python_requires='>=3.6',
)