from setuptools import setup,find_packages

setup(
    name="streamingpackagetyler1",
    version="0.1.0",
    author="Tyler Huang",
    author_email="huangyue1752@gmail.com",
    description="streaming python package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/huangyue1752/Streaming_Function.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "seaborn",
        "google-cloud",
        "asyncio",
        "azure-eventhub",
        "azure-identity",
        "aiohttp",
        "bs4"
    ],
    entry_points={
        'console_scripts':[
                'streamingpackagetyler1=src.main:main'
        ]
    },
)

