import setuptools

# read the description file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'doc/epikit-description.md'), encoding='utf-8') as f:
    long_description = f.read()

exec(open("epikit/_version.py").read())

setuptools.setup(
    name="epikit",
    version=__version__,
    author="David H. Rogers",
    author_email="dhr@lanl.gov",
    description="Cinema scientific toolset.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/epic/epikit",
    include_package_data=True,
    zip_safe=False,
    packages=[  "epikit" ],
    install_requires=[
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    scripts=[
        'doc/epikit-description.md'
    ]
)
