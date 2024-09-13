from setuptools import setup, find_packages

setup(
    name="spaceTree",  # Name of your package
    version="0.1.4",  # Version
    author="Olga Lazareva et al.",
    author_email="olazareva1993@gmail.com",
    description="PyPI package for multi-task label transfer from single-cell refrence data to spatial data",  # Short description
    long_description=open('README.md').read(),  # Long description from your README file
    long_description_content_type='text/markdown',
    url="https://github.com/PMBio/spaceTree",  # Link to your project (if available)
    packages=find_packages(),  # Automatically find and include all packages
    install_requires=[
            'numpy',
            'pandas',
            'scikit-learn',
            'scipy',
            'matplotlib',
            'seaborn',
            'h5py',
            'torch>=2.0.1',
            'torchvision',
            'torchaudio',
            'requests',
            'openpyxl',
            'absl-py',
            'aiobotocore',
            'aiohttp',
            'aiosignal',
            'anndata',
            'async-timeout',
            'attrs',
            'botocore',
            'chex',
            'cloudpickle',
            'dask',
            'dask-image',
            'datashader',
            'distributed',
            'flax',
            'geopandas',
            'infercnvpy',
            'jax',
            'jaxlib',
            'joblib',
            'pytorch-lightning',
            'scanpy',
            'scvi-tools',
            'tqdm',
            'umap-learn'
        ],
        python_requires='>=3.10',
        classifiers=[
            'Programming Language :: Python :: 3.10',
            'License :: OSI Approved :: MIT License',  # Adjust if using a different license
            'Operating System :: OS Independent',
        ],
        include_package_data=True,  # Include non-Python files specified in MANIFEST.in
    )