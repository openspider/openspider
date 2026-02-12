"""
Setup Script for Suboya TGS Curriculum
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="suboya_tgs_curriculum",
    version="1.0.0",
    author="NRT OpenSpider Team",
    author_email="opensource@openspider.ai",
    description="Suboya TGS Curriculum - Classical Wisdom + AI Education",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openspider/suboya_tgs_curriculum",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python>=3.8",
        "tqdm>=4.60.0",
        "pyyaml>=5.4.0",
    ],
    extras_require={
        "nlp": ["nltk>=3.8.0", "spacy>=3.5.0"],
        "search": ["sentence-transformers>=2.2.0", "faiss-cpu>=1.7.0"],
        "dev": ["pytest>=6.0.0"],
    },
    entry_points={
        "console_scripts": [
            "suboya-tgs=suboya_tgs_curriculum.__main__:main",
        ],
    },
)
