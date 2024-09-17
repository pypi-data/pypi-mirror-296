from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="convertcode2pdf",
    version="0.1.0",
    author="LightWheel",
    author_email="tiwariparas1096@gmail.com",
    description="A GUI tool to convert code files to PDF or TXT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/codetopdf",
    packages=find_packages(),
    install_requires=[
        "pygments",
        "weasyprint",
        "sv_ttk",
    ],
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
    entry_points={
        "console_scripts": [
            "codetopdf=codetopdf.main:main",
        ],
    },
    include_package_data=True,
    package_data={
        "codetopdf": ["resources/*"],
    },
)