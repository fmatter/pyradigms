from setuptools import setup, find_packages

requirements = open("requirements.txt", "r").read().split("\n")
setup(
    name="pyradigms",
    version="0.0.4",
    author="Florian Matter",
    author_email="florianmatter@gmail.com",
    description="Constructing and deconstructing linguistic paradigms.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/fmatter/pyradigms",
    license="GNU GPLv3",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Text Processing :: Linguistic",
    ],
    platforms="any",
    python_requires=">=3.6",
    install_requires=requirements,
    extras_require={
        "test": [
            "pytest>=5",
            "pytest-cov",
            "coverage>=4.2",
        ],
    },
)
