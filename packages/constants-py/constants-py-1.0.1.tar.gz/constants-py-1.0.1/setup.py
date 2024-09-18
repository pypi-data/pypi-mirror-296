from setuptools import setup, find_packages

setup(
    name="constants-py",
    version="1.0.1",
    author="LCreations",
    #author_email="your@email.com",
    description="Allows for the creation of constants in Python",
    #long_description="A longer description of your package",
    long_description_content_type="text/markdown",
    #url="https://github.com/your-username/your-repo",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)