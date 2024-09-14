from setuptools import setup, find_packages

setup(
    name="blikon_sdk",
    version="1.0.5",
    packages=find_packages(include=['blikon_sdk', 'blikon_sdk.*']),
    install_requires=[
        "fastapi",
        "pydantic-settings",
        "uvicorn",
        "python-jose",
        "opencensus-ext-azure",
        "setuptools"
    ],
    description="Blikon SDK for security and middleware services",
    author="Raúl Díaz Peña",
    author_email="rdiaz@yosoyblueicon.com",
    license="Blikon Ⓡ",
    url="https://github.com/blikon/blikon_sdk",
)