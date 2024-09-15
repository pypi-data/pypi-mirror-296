from setuptools import setup

with open("E:/Documents/GitHub/AutoGGUF/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="AutoGGUF",
    version="v1.8.1",
    packages=[""],
    url="https://github.com/leafspark/AutoGGUF",
    license="apache-2.0",
    author="leafspark",
    author_email="",
    description="automatically quant GGUF models",
    install_requires=required,
    entry_points={"console_scripts": ["autogguf-gui = main:main"]},
)
