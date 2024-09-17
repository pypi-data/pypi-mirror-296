from setuptools import setup, find_packages
setup(
    name="MIMDE",
    version="1.1.1",
    packages=find_packages(),
    install_requires=[],  # List your dependencies
    description="Python package for MIMDE",
    url="https://github.com/ai-for-public-services/MIMDE",
    authors="Saba Esnaashari, John Francis, and Anton Appolonov",
    author_email="sesnaashari@turing.ac.uk",
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',        # Minimum Python version required
    # Add additional metadata for publishing
    keywords="MIMDE, package, python",
    project_urls={
        "Bug Tracker": "https://github.com/ai-for-public-services/MIMDE/issues",
        "Documentation": "https://github.com/ai-for-public-services/MIMDE/wiki",
        "Source Code": "https://github.com/ai-for-public-services/MIMDE",
    },
)