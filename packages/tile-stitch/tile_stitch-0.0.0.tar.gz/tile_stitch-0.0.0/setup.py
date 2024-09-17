import setuptools

from tile_stitch.version import __version__

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='tile_stitch',
    version=__version__,
    author='jucik',
    description='blends images using three different methods',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/jucik/tile_stitch',
    packages=setuptools.find_packages(exclude=['test']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Image Processing'
    ],
    python_requires='>=3.6',
)