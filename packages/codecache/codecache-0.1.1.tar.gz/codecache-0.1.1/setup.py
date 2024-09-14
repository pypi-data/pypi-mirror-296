from setuptools import setup, find_packages
import pathlib

HERE = pathlib.Path(__file__).parent

with open(HERE / "README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="codecache",
    version="0.1.1",
    description="Provide LLMs with codebase context for improved coding assistance.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Dinesh Rai",
    author_email="drai89@gmail.com",
    url="https://github.com/dineshrai/codecache",
    packages=find_packages("src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "codecache=codecache.cli:cli",
        ],
    },
    install_requires=[
        "google-generativeai>=0.3.1",
        "click>=8.1.3",
        "python-dotenv",
        "toml",
    ],
    extras_require={
        "dev": [
            "pytest",
            "pytest-cov",
        ],
    },
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Environment :: Console",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="codebase analysis, gemini api, context caching, code summarization, cli tool, LLM, coding assistance",
    project_urls={
        "Bug Reports": "https://github.com/dineshrai/codecache/issues",
        "Source": "https://github.com/dineshrai/codecache",
    },
)
