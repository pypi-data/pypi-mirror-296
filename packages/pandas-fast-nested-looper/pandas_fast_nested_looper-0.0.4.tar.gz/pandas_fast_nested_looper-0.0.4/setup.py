import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pandas-fast-nested-looper",
    version = "0.0.4",
    author = "Ganbaatar Bold",
    author_email = "elmerganbaa@gmail.com",
    description = "pandas-fast-nested-looper",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/ganbaaelmer/pandas-fast-nested-looper.git",
    project_urls = {
        "Bug Tracker": "https://github.com/ganbaaelmer/pandas-fast-nested-looper.git",
    },
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir = {"": "src"},
    packages = setuptools.find_packages(where="src"),
    python_requires = ">=3.6"
)
