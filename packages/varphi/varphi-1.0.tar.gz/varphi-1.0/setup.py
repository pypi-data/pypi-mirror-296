from setuptools import setup, find_packages

setup(
    name='varphi',
    version='1.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'varphi=varphi.frontend.varphi:main',
        ],
    },
    install_requires=[
        "antlr4-python3-runtime",
        "varphi-tape",
    ],
)