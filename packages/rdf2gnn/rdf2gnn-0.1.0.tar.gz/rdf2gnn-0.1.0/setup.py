from setuptools import setup, find_packages

setup(
    name='rdf2gnn',  # The name of your package
    version='0.1.0',  # Initial release version
    description='A Python package for integrating RDF data with Graph Neural Networks (GNNs).',
    author='Avia Anwar',  # Replace with your name
    url='https://github.com/yourusername/rdfgnn',  # Replace with your repository URL
    packages=find_packages(exclude=['tests', 'docs']),  # Automatically find your package modules
    install_requires=[
        'torch>=1.8.0',  # PyTorch, update to the version you are using
        'torch-geometric>=2.0.0',  # PyTorch Geometric, update to the version you are using
        'rdflib>=6.0.0',  # RDFLib for handling RDF data
        'scikit-learn>=0.24.0',  # Scikit-learn for evaluation metrics
        'numpy>=1.18.0',  # NumPy, often required for scientific computing
        'scipy>=1.4.0',  # SciPy, a dependency for many scientific operations
        'pandas>=1.0.0',  # Pandas for data manipulation if used in your package
        'tqdm>=4.0.0',  # Tqdm for progress bars if used in training or processing
    ],
    python_requires='>=3.11.5',  # Specify the Python versions you support
    keywords='RDF, Graph Neural Networks, PyTorch Geometric, GNN, Machine Learning',  # Add relevant keywords
    project_urls={
        'Documentation': 'https://github.com/yourusername/rdfgnn',  # Replace with your documentation link
        'Source': 'https://github.com/yourusername/rdfgnn',
        'Tracker': 'https://github.com/yourusername/rdfgnn/issues',
    },
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',  # Ensure correct rendering of Markdown README
)
