from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="github-repo-extractor",
    version="0.1.1",
    author="Lorenzo Toscano",
    author_email="lorenzo.toscano@gmail.com",
    description="A tool to extract GitHub repositories into a single file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ltoscano/github-repo-extractor",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
    install_requires=[
        "pygithub",
        "tqdm",
        "gitpython",
    ],
)
