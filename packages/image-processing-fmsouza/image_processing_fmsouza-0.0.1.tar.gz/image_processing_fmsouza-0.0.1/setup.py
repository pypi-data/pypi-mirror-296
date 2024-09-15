from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image-processing-fmsouza",
    version="0.0.1",
    author="Felipe",
    author_email="felipe_m_souza@yahoo.com.br",
    description="Image processing Package using SKimage",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/felipefilp/image-processing-fmsouza",
    package=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)