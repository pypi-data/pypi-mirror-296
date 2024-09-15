from setuptools import setup, find_packages

setup(
    name="iyg_tools",
    version="1.0.2",
    description="",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="İlker Turan",
    author_email="ilkerturan@outlook.com",
    url="https://github.com/ilkeryolundagerek/iyg_tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
