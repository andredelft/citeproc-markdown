from setuptools import setup, find_packages


with open("README.md") as f:
    README = f.read()

setup(
    name="citeproc-markdown",
    version="0.2",
    description="Citeproc extension for Python markdown",
    long_description=README,
    long_description_content_type="text/markdown",
    author="André van Delft",
    author_email="andre@delve.nu",
    license=None,
    packages=find_packages(),
    install_requires=[
        "pyyaml>=5.4",
        "requests>=2.26",
        "ratelimit>=2.2",
        "markdown>=3.3",
        "python-decouple>=3.4",
        "json5>=0.9"
    ],
    entry_points={
        'markdown.extensions': [
            'citeproc=citeproc_markdown.citeproc:CiteprocExtension'
        ]
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3'
    ],
    include_package_data=True
)
