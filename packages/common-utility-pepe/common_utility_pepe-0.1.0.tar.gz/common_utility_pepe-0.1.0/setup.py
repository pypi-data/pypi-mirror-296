from setuptools import setup, find_packages

setup(
    name="common-utility-pepe",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
        "slack-sdk",
        "selenium"
    ],
    author="kinest1997",
    author_email="kinest1997@naver.com",
    description="korean pepe lover",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/CommonUtility",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
