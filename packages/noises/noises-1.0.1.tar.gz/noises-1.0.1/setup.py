from setuptools import setup, find_packages

with open("CHANGELOG.md","r") as ch:
    changelog = ch.read()

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="noises",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "urllib3"
    ],
    author="EscapedShadows",
    author_email="packages@escapedshadows.com",
    description="A package for generation Procedural Noises in Image form.",
    long_description=changelog + "\n\n" + long_description,
    long_description_content_type='text/markdown',
    url="https://escapedshadows.com/pythonlibs/noises.html",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)