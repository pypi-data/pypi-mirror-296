from setuptools import setup, find_packages

setup(
    name="baats",
    version="0.1.0",
    description="Una librería para esconder cosas en archivos.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Carlos-dev-G",
    author_email="baa4tsdev@example.com",
    url="https://github.com/Carlos-dev-G/baats",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
