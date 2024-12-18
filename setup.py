from setuptools import setup

setup(
    name='cardinality',
    version='0.0.1',
    packages=['src'],
    entry_points={
        "console_scripts": [
            "cardinality=main:main",
        ]
    },
    install_requires=[
        "contourpy==1.3.0",
        "cycler==0.12.1",
        "fonttools==4.55.3",
        "importlib_resources==6.4.5",
        "kiwisolver==1.4.7",
        "matplotlib==3.9.4",
        "numpy==2.0.2",
        "packaging==24.2",
        "pillow==11.0.0",
        "pyparsing==3.2.0",
        "python-dateutil==2.9.0.post0",
        "randomhash==0.6.0",
        "six==1.17.0",
        "xxhash==3.5.0",
        "zipp==3.21.0",
    ],
)