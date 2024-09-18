from setuptools import setup, find_packages

setup(
    name='rdf2gnn',  # The name of your package
    version='0.1.1',  # Initial release version
    description='A Python package for integrating RDF data with Graph Neural Networks (GNNs).',
    author='Avia Anwar',  # Replace with your name
    url='https://github.com/DataDrivenCPS/rdf2gnn',  # Replace with your repository URL
    packages=find_packages(),  # Automatically find your package modules
    install_requires=[
        "torch>=2.4.0",
        "torch-geometric>=2.6.0",
        "rdflib>=7.0.0",
        "numpy>=2.0",
        "scikit-learn>=1.5.2",
        "pandas>=2.0.3",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

