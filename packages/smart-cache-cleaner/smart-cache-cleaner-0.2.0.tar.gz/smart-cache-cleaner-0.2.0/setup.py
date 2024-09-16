from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="smart-cache-cleaner",
    version="0.2.0",
    author="Sean Michael",
    author_email="hommeunix@gmail.com",
    description="A cross-platform utility for cleaning cache and temporary files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/M43K-10GBASE-SR/smart-cache-cleaner",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.6",
    install_requires=[
        "psutil",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "smart-cache-cleaner=smart_cache_cleaner.main:main",
        ],
    },
)
