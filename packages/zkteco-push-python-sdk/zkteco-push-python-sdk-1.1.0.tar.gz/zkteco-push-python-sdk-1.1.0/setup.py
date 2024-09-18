### setup.py
from setuptools import setup, find_packages

setup(
    name='zkteco-push-python-sdk',
    version='1.1.0',
    description='A Python SDK for ZKTeco Attendance Pull Communication Protocol',
    author='Vincent Luba',
    author_email='vincent@biz-4-africa.com',
    url='https://github.com/EtsBIZ4Africa/zkteco-push-python-sdk',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
