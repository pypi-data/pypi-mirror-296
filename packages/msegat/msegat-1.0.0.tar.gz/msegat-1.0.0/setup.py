import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

requires = [
    "requests>=2.31.0",
    "python-dateutil>=2.8.2",
    "jsonpickle>=3.0.2",
    "urllib3>=1.26",
    "six>=1.16.0",
]

setuptools.setup(
    name="msegat",
    version="1.0.0",
    description="Msegat API client",
    author="Abdullah Alaidrous",
    author_email="abd.alaidrous@gmail.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/abdroos/msegat",
    package_dir={"msegat": "msegat"},
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=requires,
    classifiers=classifiers,
)
