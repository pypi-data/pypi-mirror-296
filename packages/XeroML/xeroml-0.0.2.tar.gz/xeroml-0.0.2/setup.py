"""
Setup script for XeroML.
"""
import sys

# Check if setuptools is installed
try:
    from setuptools import setup, find_packages
except ImportError:
    print("setuptools is required to install XeroML. Please install it first.")
    sys.exit(1)

# Check Python version
if not (sys.version_info[0] == 3 and sys.version_info[1] >= 9):
    sys.exit(
        f'XeroML requires Python 3.9 or higher. '
        f'You are using Python {sys.version_info[0]}.{sys.version_info[1]}.'
    )

# Read long description from README.md
try:
    with open("README.md", "r", encoding="utf-8") as fh:
        long_description = fh.read()
except FileNotFoundError:
    long_description = ("XeroML is currently under development")

# Main setup configuration
setup(
    name='XeroML',
    version='0.0.2',
    author='Julhash Kazi',
    author_email='XeroML@kazilab.se',
    url='https://www.kazilab.se',
    description="A data management platform",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='Apache-2.0',
    install_requires=[
        'pandas==2.2.2',
        'numpy==1.26.4',
        'scipy==1.13.0',
        'matplotlib==3.8.2',
        'statsmodels==0.14.0',
        'scikit-learn==1.4.2',
        'xgboost==1.7.6',
        'seaborn==0.13.1',
        'torch==2.1.2',
        'nimfa==1.4.0',
        'optuna==3.3.0',
        'ipywidgets==8.0.4',
        'joblib==1.2.0',
        'tqdm==4.65.0',
        'catboost==1.2.5',
        'imbalanced-learn==0.12.2',
        'IPython==8.20.0',
        'kaleido==0.2.1',
        'lime==0.2.0.1',
        'lightgbm==4.3.0',
        'openpyxl==3.1.2',
        'plotly==5.21.0',
        'scikit-optimize==0.8.1',
        'shap==0.45.0',
        'tensorflow==2.16.1'
    ],
    platforms='any',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
    python_requires='>=3.9',  # Ensure this matches your compatibility checks
)
