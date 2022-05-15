import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="fastapi-lowlevel-pagination",
    version="0.0.1",
    author="LooLzzz",
    author_email="noaml12@hotmail.com",
    description="A fastapi lowlevel pagination system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/LooLzzz/fastapi-lowlevel-pagination",
    project_urls={
        "Bug Tracker": "https://github.com/LooLzzz/fastapi-lowlevel-pagination/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(include=["fast_pagination", 'fast_pagination.*']),
    install_requires=['fastapi'],
    python_requires=">=3.6",
)
