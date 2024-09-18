from setuptools import setup, find_packages

setup(
    name="pyjcore",                # Package name
    version="1.0.1",                      # Package version
    packages=find_packages(),             # Automatically find packages
    install_requires=[],                  # List dependencies here (if any)
    author="Sariya Ansari",
    author_email="",
    description="A Python package that mimics Core Java collection classes",
    long_description=open("README.md").read(),  # Long description from README
    long_description_content_type="text/markdown",
    url="https://github.com/Sariya-Ansari/pyjcore.git",  # Link to your project repository
    classifiers=[                        # Metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',              # Minimum Python version
)