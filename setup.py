from setuptools import setup, find_packages

setup(
    name="bitget",
    version="1.0.0",
    author="Bitget",
    description="SDK da API V3 da Bitget",
    packages=find_packages(),
    install_requires=[
        "requests",  # Adiciona requests como dependência
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)