from setuptools import setup, find_packages


with open("README.md") as f:
    README = f.read()

with open('requirements.txt') as f:
    REQUIREMENTS = f.read().splitlines()

setup(
    name="citeproc-markdown",
    version="0.1",
    description="Citeproc extension for Python markdown",
    long_description=README,
    author="André van Delft",
    author_email="andre@delve.nu",
    license=None,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    entry_points={
        'markdown.extensions': [
            'citeproc=citeproc_markdown.citeproc:CiteprocExtension'
        ]
    },
    include_package_data=True
)
