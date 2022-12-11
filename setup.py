"""Setup module for aioqsw."""
from pathlib import Path

from setuptools import setup

PROJECT_DIR = Path(__file__).parent.resolve()
README_FILE = PROJECT_DIR / "README.md"
VERSION = "0.3.0"


setup(
    name="aioqsw",
    version=VERSION,
    url="https://github.com/Noltari/aioqsw",
    download_url="https://github.com/Noltari/aioqsw",
    author="Álvaro Fernández Rojas",
    author_email="noltari@gmail.com",
    description="Library to control QNAP QSW devices",
    license="Apache-2.0",
    long_description=README_FILE.read_text(encoding="utf-8"),
    long_description_content_type="text/markdown",
    packages=["aioqsw"],
    python_requires=">=3.9",
    include_package_data=True,
    install_requires=["aiohttp"],
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Home Automation",
    ],
)
