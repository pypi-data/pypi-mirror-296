from setuptools import setup, find_packages

setup(
    name='TiRank',  # Replace with your own package name
    version='0.6',  # Package version
    author='Lenis Lin',  # Replace with your name
    author_email='727682308@qq.com',  # Replace with your email
    license='MIT License',
    description='A comprehensive analysis tool for transfering phenotype of bulk transcritomic data to single cell or spatial transcriptomic data.',  # Short description
    long_description=open('README.md').read(),  # Long description read from the the readme file
    long_description_content_type='text/markdown',  # Specify the content type as Markdown
    url='https://github.com/LenisLin/TiRank',  # URL to your package's repository
    packages=find_packages(include=['TiRank']),  # List of all Python import packages that should be included in the Distribution Package
    include_package_data=True,
    install_requires=[
        'torch',
        'torchvision',
        'optuna==3.4.0',

        'numpy==1.22.3',
        'scipy==1.8.1',
        'pandas==1.5.3',
        'leidenalg',

        'scikit-learn==1.0.2',
        'lifelines==0.27.8',
        'statsmodels==0.14.0',
        'imbalanced-learn==0.11.0',

        'matplotlib==3.7.1',
        'seaborn==0.12.2',
        'pillow==9.4.0',

        'scanpy==1.9.5',
        'gseapy==1.1.1',

        'dash==2.14.2',
        'dash-bootstrap-components==1.5.0',
        'dash-loading-spinners==1.0.3'
    ],
    classifiers=[
        # Classifiers help users find your project by categorizing it.
        # For a list of valid classifiers, see https://pypi.org/classifiers/
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Example license
    ],
    python_requires='>=3.9',  # Minimum version requirement of the package
)