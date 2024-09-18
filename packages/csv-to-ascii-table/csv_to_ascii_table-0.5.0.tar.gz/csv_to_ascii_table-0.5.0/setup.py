from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="csv-to-ascii-table",
    version="0.5.0",
    author="Benjamin Cance",
    author_email="canceb@gmail.com",
    description="An asynchronous CSV to ASCII table converter",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rowingdude/ascii_table_generator",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "asyncio",
    ],
    entry_points={
        "console_scripts": [
            "csv-to-ascii=csv_to_ascii_table.converter:main",
        ],
    },
)