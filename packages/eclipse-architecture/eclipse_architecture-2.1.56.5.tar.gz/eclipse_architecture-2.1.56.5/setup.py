from setuptools import setup, find_packages

setup(
    name="eclipse-architecture",  # Replace with your package name
    version="2.1.56.5",  # Your package version
    author="TNSA Artificial Intelligence",
    author_email="tnsa.company@gmail.com",
    description="TNSA Standard is a MuiltiModal Development Framework developed by TNSA AI ",
    long_description_content_type="text/markdown",
    url="https://tnsaai.github.io/home/",  # GitHub or project URL
    packages=find_packages(),  # Automatically find your package
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Minimum Python version requirement
)
