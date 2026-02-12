"""
Setup Script for Athenian Digital Academy
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="athenian_digital_academy",
    version="1.0.0",
    author="NRT OpenSpider Team",
    author_email="opensource@openspider.ai",
    description="Athenian Digital Academy - Multi-Agent System for Digital Scientists",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openspider/athenian_digital_academy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.8",
    install_requires=[
        "python>=3.8",
        "numpy>=1.19.0",
        "pandas>=1.2.0",
        "dataclasses>=0.6; python_version<'3.7'",
        "tqdm>=4.60.0",
        "pyyaml>=5.4.0",
    ],
    extras_require={
        "ml": ["torch>=1.8.0", "transformers>=4.5.0"],
        "api": ["openai>=0.27.0", "anthropic>=0.3.0"],
        "vector": ["faiss-cpu>=1.7.0"],
        "dev": ["pytest>=6.0.0", "pytest-cov>=2.0.0"],
    },
    entry_points={
        "console_scripts": [
            "athenian-academy=athenian_digital_academy.__main__:main",
        ],
    },
    include_package_data=True,
    package_data={
        "athenian_digital_academy": ["config/*.yaml"],
    },
)
