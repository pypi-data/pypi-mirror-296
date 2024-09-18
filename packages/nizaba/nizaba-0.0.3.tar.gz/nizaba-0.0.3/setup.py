from setuptools import setup, find_packages

setup(
    name="nizaba",
    version="0.0.3",
    author="Arcadia78 Solutions",
    author_email="david@arcadia78.com",
    description="Python library for Nizaba",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[ ],
    include_package_data=True,
)
