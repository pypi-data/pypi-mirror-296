from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="text_analysis_tools",  # Nom du package
    version="0.1.0",  # Version initiale
    author="Ton Nom",
    author_email="zakiyoubababodi@gmail.com",
    description="Un package Python pour la manipulation de texte",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Zakiyou/text_toolkit.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
