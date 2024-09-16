from setuptools import find_packages, setup

__package_name__ = 'RaspyTweak'
__author__ = 'Voyager'
__version__ = '0.0.0.1a2'
__version_prefix__ = 'pre-alpha'
__doc__  = 'A library for raspberry pi'

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name=__package_name__,
    version=__version__,
    description=__doc__,
    package_dir=dict({"": __package_name__}),
    packages=find_packages(where=__package_name__),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    author=__author__,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
    ],
    python_requires=">=3.10",
    license='MIT',
    url="https://github.com/voyager-2021/RaspyTweak",
    download_url=f"https://github.com/voyager-2021/RaspyTweak/releases/tag/pre-alpha",
    project_urls={
        "Issues": "https://github.com/voyager-2021/RaspyTweak/issues"
    },
    requires=[
        "psutil",
        "deprecated",
        "wrapt"
    ]
)
