from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Processing-of-image-package",
    version="0.0.1",
    author="Ray_King",
    author_email="raytoyagami25@gmail.com",
    description="Python package template with multiple modules",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ray-King11/Processing-of-image-package",
    packages=find_packages(),
    install_requires=[
        'Pillow',
        'opencv-python',
        'scikit-image',
    ],
    python_requires='>=3.6',
)
