from setuptools import setup, find_packages

setup(
    name='aeroterra_ds',
    version='2.3.5',
    author='Data Science',
    author_email='aeroterra_ds@aeroterra.com',
    description='Python Functions To Work With GeoSpatial Data & ArcGis in a simpler way',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://example.com',
    package_dir={'': "src"},
    packages=find_packages("src"),
    classifiers=[
        'Programming Language :: Python :: 3',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    keywords='arcgis',
    python_requires='>=3.9',
    install_requires=[
        "gssapi",
        "dask",
        "dask[dataframe]",
        "arcgis",
        "pyproj",
        "shapely",
        "matplotlib",
        "geopandas",
        "pandas",
        "haversine",
        "rasterio",
        "rtree"
    ],
)
