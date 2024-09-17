from setuptools import setup, find_packages

setup(
    name="depviz",
    version="1.0.4",
    description="Quick Dependency Graph Viewer",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/depviz",  # Update with your repo URL
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=7.0",
        "graphviz>=0.14",
    ],
    entry_points="""
        [console_scripts]
        depviz=depviz.cli:main
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update if using a different license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
