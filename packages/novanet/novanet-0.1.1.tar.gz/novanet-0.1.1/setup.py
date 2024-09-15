from setuptools import setup, find_packages

setup(
    name="novanet",               # Package name
    version="0.1.1",                 # Initial version
    author="Soumick Sarker",
    author_email="soumicksarker9@gmail.com",
    description="novanet is a package for image segmentation",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/soumick1/NovaNet",  # Your GitHub or project URL
    packages=find_packages(),         # Automatically finds and includes all packages
    install_requires=[                # Your dependencies
        'numpy',
        'pandas',
        'torch',
        'PyYAML',
        'albumentations',
        'tqdm',
        'matplotlib',
        'opencv-python',
        'scikit-learn'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    entry_points={
        'console_scripts': [
            'train_model=my_package.main:main',  # Creates a CLI command for the training script
        ],
    },
)