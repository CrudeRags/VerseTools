import setuptools

with open("README.md",'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name="verse_tools-CrudeRags",
    version="0.0.1",
    author="Crude Rags",
    author_email="crude.rags@gmail.com",
    description="A package to get verses from different languages given reference in English",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrudeRags/VerseTools",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL v3 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)