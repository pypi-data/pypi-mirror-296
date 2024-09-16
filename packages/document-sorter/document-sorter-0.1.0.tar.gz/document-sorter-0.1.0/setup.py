from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="document-sorter",
    version="0.1.0",
    author="Jazmia",
    author_email="jazmia.henry@google.com",
    description="A package to automatically sort documents into folders based on content similarity",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jazmiahenry/document_sorter",
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "document-sorter=document_sorter.main:main",
        ],
    },
)