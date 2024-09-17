"""A module which goes through the setup of files"""
from setuptools import setup, find_packages


def parse_meta(path_to_meta):
    """
    A function to parse through meta.py file

    path_to_meta: string
        metadata path.

    returns metadata from meta.py file

    """
    with open(path_to_meta) as f:
        meta = {}
        for line in f.readlines():
            if line.startswith("__version__"):
                meta["__version__"] = line.split('"')[1]
    return meta


meta = parse_meta("hvspatialpy/meta.py")

with open("README.md", encoding="utf8") as f:
    long_description = f.read()

setup(
    name='hvspatialpy',
    version=meta['__version__'],
    description='A python package for evaluating the spatial variability of a site utilizing the Horizontal-to-Vertical Spectral Ratio (HVSR)',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/fjornelas/hvspatialpy',
    license='GNU General Public License v3',
    author='Francisco Javier Ornelas',
    author_email='jornela1@g.ucla.edu',
    classifiers=[
        'Development Status :: 5 - Production/Stable',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Topic :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Physics',

        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

        'Natural Language :: English',

        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Topic :: Software Development :: Version Control :: Git',
    ],
    keywords='HVSR, geospatial statistics, spatial variability',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=['numpy>=1.20', 'pandas<1.5.4', 'matplotlib', 'obspy', 'scipy',
                      'parzenpy', 'tslearn', 'scikit-learn', 'rasterio', 'ipywidgets', 'IPython'],
    project_urls={
        'Bug Reports': 'https://github.com/fjornelas/hvspatialpy/issues',
        'Source': 'https://github.com/fjornelas/hvspatialpy/',
        'Docs': 'https://fjornelas.github.io/hvspatialpy/'
    },
)
