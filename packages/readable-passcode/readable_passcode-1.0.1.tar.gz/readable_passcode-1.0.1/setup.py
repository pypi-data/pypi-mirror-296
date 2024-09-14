from setuptools import setup, find_packages

setup(
    name="readable_passcode",
    version="1.0.1",
    author="Deden",
    author_email="mail@dedenbangkit.com",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    description="Generate human-readable passcodes with memory optimization",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    project_urls={
        "Documentation": "https://github.com/dedenbangkit/readable-passcode",
        "Bug Reports": "https://github.com/dedenbangkit/readable-passcode/issues",
        "Source Code": "https://github.com/dedenbangkit/readable-passcode",
    },
    url="https://github.com/dedenbangkit/readable-passcode",
    include_package_data=True,
    install_requires=[],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    package_data={
        "readable_passcode": ["words.txt"],
    },
    entry_points={
        "console_scripts": [
            "readable-passcode=readable_passcode.readable_passcode:cli",
        ],
    },
    extras_require={
        "dev": ["check-manifest"],
    },
    python_requires=">=3.8",
)
