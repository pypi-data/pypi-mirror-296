import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

with open("requirements.txt", "r") as fin:
    REQS = fin.read().splitlines()

with open("requirements-dev.txt", "r") as fin:
    REQS_DEV = [item for item in fin.read().splitlines() if not item.endswith(".txt")]

setuptools.setup(
    name="ai-data-preprocessing-queue",
    version="1.5.0",
    description="Can be used to pre process data before ai processing",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/SamhammerAG/ai_data_preprocessing_queue",
    author="Samhammer AG",
    author_email="support@samhammer.de",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development",
    ],
    keywords="text processing,ai",
    packages=setuptools.find_packages(exclude=["tests"]),
    package_data={"ai_data_preprocessing_queue": ["py.typed"]},
    python_requires=">=3.12",
    install_requires=REQS,
    extras_require={"dev": REQS_DEV},
    project_urls={
        "Documentation": "https://github.com/SamhammerAG/ai_data_preprocessing_queue",
        "Bug Reports": "https://github.com/SamhammerAG/ai_data_preprocessing_queue/issues",
        "Source": "https://github.com/SamhammerAG/ai_data_preprocessing_queue",
    },
)
