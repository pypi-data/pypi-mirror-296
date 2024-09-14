from setuptools import setup, find_packages

setup(
    name="mypackage0917",
    version="0.1.0",
    description="A simple example Python package",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/mypackage",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[                      # 依赖的库
            'requests',                         # 示例依赖
            'pandas',
            'openai',
            'ragchecker',
            'spacy',
        ],
    python_requires='>=3.10',
)