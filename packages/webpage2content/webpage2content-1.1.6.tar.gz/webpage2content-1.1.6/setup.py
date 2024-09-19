import os
from setuptools import setup, find_packages


# Read the version from the VERSION file
with open(
    os.path.join(os.path.dirname(__file__), "webpage2content/VERSION"), "r"
) as version_file:
    version = version_file.read().strip()


setup(
    name="webpage2content",
    version=version,
    author="Mikhail Voloshin",
    author_email="mvol@mightydatainc.com",
    description="A simple Python package to extract text content from a webpage.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mighty-Data-Inc/webpage2content",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "html2text",
        "openai",
        "python-dotenv",
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    entry_points={
        "console_scripts": [
            "webpage2content=webpage2content.webpage2content_impl:main",
        ],
    },
    license="Apache-2.0",
    package_data={
        "webpage2content": ["VERSION"],
    },
    include_package_data=True,
)
