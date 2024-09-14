from setuptools import setup, find_packages

setup(
    name="picsumphotos",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    author="EscapedShadows",
    author_email="packages@escapedshadows.com",
    description="A package for image processing utilities using the Picsum API",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://escapedshadows.com/pythonlibs/picsumphotos.html",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)