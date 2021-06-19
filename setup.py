import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lightningaddon",
    version="0.0.1",
    author="Subhaditya Mukherjee",
    author_email="msubhaditya@gmail.com",
    description="Add ons for pytorch lightnin",
    license="GPLv3+",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SubhadityaMukherjee/lightningAddOns",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
