from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="climate_hurricane_analysis",
    version="0.1.2",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scipy",
        "xarray",
        "netCDF4",
        "scikit-learn",
        "matplotlib",
    ],
    author="Rohan Marangoly",
    author_email="rohan@climate.ai",
    description="A package for hurricane analysis using SST data.",
    long_description=long_description, 
    long_description_content_type="text/markdown",
    url="https://github.com/ClimateAI/cyclone_package",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
