from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="games_in_python",
    version="0.0.1",
    author="Pedro Thezi",
    author_email="pedro.maschieto130@gmail.com",
    description="A package with some games in python",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PedroThezi/package-games-in-python",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8',
)