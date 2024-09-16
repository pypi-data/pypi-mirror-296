from setuptools import setup, find_packages

setup(
    name="my_python_package24",
    version="1.0.1",
    author="Lamrin",
    author_email="ahirwarnirmal2017@gmail.com",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/nirmalkahirwar/my_python_package24",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
    ],
    python_requires=">=3.6"
)
