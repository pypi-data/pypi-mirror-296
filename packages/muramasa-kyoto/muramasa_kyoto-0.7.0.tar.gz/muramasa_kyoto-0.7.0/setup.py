from setuptools import setup, find_packages

setup(
    name="muramasa-kyoto",
    version="0.7.0",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "scikit-learn",
        "scipy",
        "joblib",
    ],
    package_data={
        'muramasa': ['data/addgene_6018.csv', 'trained_model.joblib'],
    },
    author="Rei Suzawa",
    author_email="reisuzawa.0725@gmail.com",
    description="A package for plasmid DNA sequence anomaly detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://gitlab.igem.org/2024/software-tools/kyoto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)