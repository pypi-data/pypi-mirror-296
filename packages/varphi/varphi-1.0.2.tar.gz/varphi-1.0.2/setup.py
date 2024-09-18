from setuptools import setup, find_packages

setup(
    name="varphi",
    version="1.0.2",
    description="A package for parsing and evaluating Turing programs.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Hassan El-Sheikha",
    author_email="hassan.elsheikha@utoronto.ca",
    url="https://github.com/hassanelsheikha/varphi",
    packages=find_packages(),
    install_requires=[
        "varphitape",
        "antlr4-python3-runtime"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'varphi=varphi.frontend.varphi:main',
        ],
    },
    python_requires='>=3.12',
    include_package_data=True,
)
