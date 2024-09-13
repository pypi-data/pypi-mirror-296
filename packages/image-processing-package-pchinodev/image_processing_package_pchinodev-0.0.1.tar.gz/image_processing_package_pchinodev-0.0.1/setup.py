from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_package_pchinodev",
    version="0.0.1",
    author="pierr_chino",
    author_email="pchinol11@gmail.com",
    description="A package for image processing",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pchinodev/image_processing_package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.10',
)