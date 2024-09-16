
from setuptools import setup, find_packages

setup(
    name="binaryflow",  # Name of the package
    version="1.1.1",  # Version follows Semantic Versioning
    author="Krishna Gopal Jha",  # Your name
    description="A custom file transmission utility based on the Binary Flow Protocol for transferring files using IP and hostname.",
    long_description=open('README.md').read(),  # Reads the long description from the README file
    long_description_content_type='text/markdown',  # Ensures the README file is interpreted as markdown
    url="https://github.com/krishnagopaljha/binaryflow",  # Optional: GitHub repository URL
    packages=find_packages(),  # Automatically discover packages (looks for the 'ftp' folder and others)
    install_requires=[],  # Add any dependencies here if needed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Ensure compatibility with Python 3.6 and above
)
