from setuptools import setup, find_packages

setup(
    name='tcr-boost',
    version='0.1.0',
    description='T-Cell Receptor Bayesian Optimization of Specificity and Tuning',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/yourusername/tcr-boost',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'torch',
        'gpytorch',
        'botorch',
        'esm',
        'numpy',
        'scikit-learn',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
