"""
D-LIM (Direct Latent Interpretable Model): An interpretable neural network for
mapping genotype to fitness.

D-LIM employs a constrained latent space to map genes to single-value
dimensions, enabling the extrapolation to new genotypes and capturing the
non-linearity in genetic data. Its design facilitates a deeper understanding of
genetic mutations and their impact on fitness, making it highly applicable in
molecular adaptations.
"""

from setuptools import setup, find_packages

setup(
    name='dlim',
    version='1',
    packages=find_packages(),
    install_requires=[
        "pandas",
        "torch",
        "numpy",
    ],
    # Other metadata
    author='Shuhui Wang, Alexandre Allauzen, Philippe Nghe, Vaitea Opuu',
    author_email='vaiteaopuu@gmail.com',
    description='Model genotype to fitness map',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="MIT",
    url="https://github.com/LBiophyEvo/D-LIM-model"
)
