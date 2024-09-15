from setuptools import setup, find_packages

setup(
    name='varphi',
    version='0.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'varphi=Varphi.frontend.varphi:main',
        ],
    },
    install_requires=[
        "antlr4-python3-runtime",
        "VarphiTape",
    ],
)