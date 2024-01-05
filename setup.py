from setuptools import setup


setup(
    name='pkvid',
    description='Python package intended to help with automation of video editing',
    version='0.1.0',
    packages=['pkvid'],
    entry_points={
        'console_scripts': [
            'pkvid = pkvid.cli:main'
        ]
    },
)
