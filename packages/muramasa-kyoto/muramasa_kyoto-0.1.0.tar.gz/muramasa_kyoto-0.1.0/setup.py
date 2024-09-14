from setuptools import setup, find_packages

setup(
    name="muramasa-kyoto",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for plasmid DNA sequence anomaly detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/muramasa",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)