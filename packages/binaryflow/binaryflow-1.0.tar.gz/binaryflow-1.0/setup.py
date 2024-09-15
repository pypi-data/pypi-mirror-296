from setuptools import setup, find_packages

setup(
    name="binaryflow",  # Name of the package
    version="1.0",  # Initial release version
    author="Krishna Gopal Jha",  # Your name
    description="A custom File transmission utility based of Binary FLow Protocolfor file transfer using IP and hostname.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/krishnagopaljha/binaryflow",  # Optional: GitHub URL if available
    packages=find_packages(),  # Finds the 'ftp' folder and its files (client.py and server.py)
    install_requires=[],  # Dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved ",
        "License :: OSI Approved :: Apache Software License",
    ],
    python_requires='>=3.6',
)
