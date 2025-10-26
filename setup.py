from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wearables-sdk",
    version="1.0.0",
    author="Wearables SDK Team",
    author_email="dev@wearables-sdk.example.com",
    description="Secure edge timestamping for wearable devices",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/wearables-sdk",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Medical Science Apps",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": ["pytest>=6.0", "black", "flake8"],
        "legacy": ["pysha3>=1.0.2"],  # For Python < 3.6
    },
)
