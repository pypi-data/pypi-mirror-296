from setuptools import setup, find_packages

setup(
    name="HF_QuickUtils",
    version="0.1.1",
    author="MCqie",
    author_email="qq1051846107@outlook.com",
    description="A utils pack for downloading model form Huggingface mirror site in china",
    packages=find_packages(),
    install_requires=[
        "setuptools~=72.1.0",
        "transformers~=4.44.2",
        "huggingface-hub~=0.24.7"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
