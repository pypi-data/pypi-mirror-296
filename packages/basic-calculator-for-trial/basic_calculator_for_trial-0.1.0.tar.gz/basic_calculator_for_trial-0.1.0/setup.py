from setuptools import setup, find_packages

setup(
    name="basic_calculator_for_trial",
    version="0.1.0",
    author="Pallavi Hoge",
    author_email="pallavihoge47@gmail.com",
    description="A simple Python calculator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/pallavihoge1/basic_calculator_for_trial",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
