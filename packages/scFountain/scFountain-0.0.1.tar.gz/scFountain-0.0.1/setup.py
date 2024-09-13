
# encoding=utf-8
from setuptools import setup, find_packages
import pathlib

#here = pathlib.Path(__file__).parent.resolve()

setup(
    name="scFountain",
    version="0.0.1",
    description="Rigorous integration of single-cell ATAC-seq data using regularized barycentric mapping",
    license="MIT Licence",
    url="https://github.com/BioX-NKU/Fountain",
    author="BioX-NKU",
    classifiers=[
        "Programming Language :: Python :: 3.9",
    ],
    keywords="scATAC-seq, batch integration, barycentric mapping, online integration, cell type-specific implication",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        'anndata>=0.8.0',
        'scanpy>=1.9.1',
        'torch>=1.12.1',
        'pandas>=1.4.2',
        'scikit-learn>=1.0.2',
        'numpy>=1.21.5',
        'scipy>=1.9.3',
        'episcanpy>=0.3.2',
        'tqdm>=4.28.1',      
    ]
)






