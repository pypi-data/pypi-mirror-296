from setuptools import setup, find_packages

setup(
    name='PlotMagic',
    version='0.1',
    description='A Python package for easy-to-use advanced visualizations',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'matplotlib',
        'seaborn',
        'numpy',
        'pandas',
    ],
    python_requires='>=3.6',
)
