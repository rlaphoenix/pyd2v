from setuptools import setup, find_packages

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name="pyd2v",
    version="1.0.1",
    author="PHOENiX",
    author_email="pragma.exe@gmail.com",
    description="A Python Parser for DGMPGDec's D2V Project Files",
    license="MIT",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/rlaPHOENiX/pyd2v",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
