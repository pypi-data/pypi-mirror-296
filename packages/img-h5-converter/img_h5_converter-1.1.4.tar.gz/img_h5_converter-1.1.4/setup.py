from setuptools import setup, find_packages
from pathlib import Path


this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup (
    
    name= 'img_h5_converter',
    version= '1.1.4',
    description= 'To convert an image to HDF5 file format which can be then sent and converted back to any of the image format.',
    long_description= long_description,
    long_description_content_type = 'text/markdown',
    author = 'Archit Mishra',
    url= 'https://github.com/architmishra-15/Projects/tree/main/img_converter',
    packages= find_packages(),
    install_requires = [
        'numpy',
        'Pillow',
        'h5py',
    ],
    
    classifiers= [
        
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    
    python_requires='>=3.6',
)