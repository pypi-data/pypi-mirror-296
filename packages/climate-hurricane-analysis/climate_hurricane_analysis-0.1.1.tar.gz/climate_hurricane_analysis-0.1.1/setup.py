from setuptools import setup, find_packages

setup(
    name="climate_hurricane_analysis",
    version="0.1.1",
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
    long_description="",
    url="https://github.com/ClimateAI/cyclone_package",  # Update with your URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
