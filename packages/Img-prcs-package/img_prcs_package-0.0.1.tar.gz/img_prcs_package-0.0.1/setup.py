from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Img_prcs_package",
    version="0.0.1",
    author="Dev_yuji",
    author_email="milsonyujiaoki.estudos@gmail.com",
    description="I'm a software development student",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Milsonyujiaoki/image-processing-package",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
    )