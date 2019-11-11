import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyradigms",
    version="0.0.2",
    author="Florian Matter",
    author_email="florianmatter@gmail.com",
    description="Creates paradigms from a table of entries with parameters.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/florianmatter/pyradigms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)