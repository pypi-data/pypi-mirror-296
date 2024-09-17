from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

install_requires = ['numpy', 'scipy', 'scikit-learn', 'qpsolvers', 'cvxopt', 'torch', 'matplotlib']

setup(
    name='quantes',
    version="2.0.8",
    packages=find_packages(),
    author="Wenxin Zhou",
    author_email="wenxinz@uic.edu",
    description="Convolution Smoothed Quantile and Expected Shortfall Regression",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WenxinZhou/quantes",  # replace with the URL of your project
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_data={
        '': ['*.txt', '*.rst'],
        'hello': ['*.msg'],
    },
    install_requires=install_requires,
)
