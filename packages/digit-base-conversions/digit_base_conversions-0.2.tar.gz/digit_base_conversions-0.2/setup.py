from setuptools import setup,find_packages

setup(
    name="digit_base_conversions",  # Choose a unique name for your package
    version="0.2",  # Increment the version with each update
    description="A Python module for converting numbers into list of digits in a given base.",
    author="Olger Männik",
    author_email="olgerm@protonmail.com",
    url="https://github.com/Olle7/digit_base_conversions",  # Optional GitHub URL
    #py_modules=["digit_base_conversions"],  # Your module's name
    #classifiers=[
    #    "Programming Language :: Python :: 3",
    #    "License :: OSI Approved :: MIT License",  # Choose your preferred license
    #    "Operating System :: OS Independent",
    #],
    #python_requires=">=3.6",
    packages=find_packages(),
    install_requires=[],
)
