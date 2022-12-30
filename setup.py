from setuptools import setup, find_packages

PACKAGE_NAME = 'swellpy'
VERSION = '0.0.1'

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    author='Greg Hoskin, Mustafa Hoda',
    author_email='greg@swell.is, mustafa@swell.is',
    packages=find_packages(),
    install_requires=[
        'requests',
        'requests_toolbelt',
        'ratelimit'
    ]
)