from setuptools import setup, find_packages

setup(
    name="MIMDE",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],  # List your dependencies
    description="Python package for MIMDE",
    url="https://github.com/ai-for-public-services/MIMDE",
    authors="Saba Esnaashari, John Francis, and Anton Appolonov",
    author_email="your_email@example.com",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    # Add additional metadata for publishing
    keywords="MIMDE, package, python",
    project_urls={
        "Bug Tracker": "https://github.com/ai-for-public-services/MIMDE/issues",
        "Documentation": "https://github.com/ai-for-public-services/MIMDE/wiki",
        "Source Code": "https://github.com/ai-for-public-services/MIMDE",
    },
)