import setuptools

with open("README.md", "r", encoding = "utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "semroute",
    version = "1.0.1",
    author = "Hansal Shah",
    author_email = "hansalshah100@gmail.com",
    description = "SemRoute is a semantic router that helps you route using the semantic meaning of the query",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/HansalShah007/semroute",
    project_urls = {
        "Issues": "https://github.com/HansalShah007/semroute/issues",
    },
    packages = setuptools.find_packages(),
    install_requires=[
        'openai>=1.35.10',
        'numpy>=2.0.0',
        'mistralai>=0.4.2',
        'pydantic>=2.8.2'
    ],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.10"
)