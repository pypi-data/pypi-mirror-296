from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hydrogapai",
    version="0.6.0",
    author="Konstantinos Perifanos, Yiannis Kontons, Konstantinos Plataridis",
    author_email="kostas.perifanos@gmail.com, ykontos81@gmail.com, platarid@gmail.com",
    description="HydroGAP-AI: Hydro-Gap Artificial Intelligence",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kperi/HydroGAP-AI",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[
        "numpy",
        "pandas>=2.2.2",
        "scipy",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "xgboost",
        "lightgbm",
        "hydroeval",
        "statsmodels",
        "scipy",
        "tqdm", 
    ],
)