from setuptools import setup, find_packages # type: ignore

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt", "r") as f:
    requirements = f.read().splitlines()

setup(
    name="image_processing_mr",
    version="0.0.1",
    author="Mateus",
    description="Image processing package using Skimage",
    long_description="page_description",
    long_description_content_type="text/markdown",
    url="https://github.com/mateusrr/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.5',
)