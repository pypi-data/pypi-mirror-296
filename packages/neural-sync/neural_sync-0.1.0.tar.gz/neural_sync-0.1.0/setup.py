# from setuptools import setup
#
# if __name__ == "__main__":
#     setup()

from setuptools import setup, find_packages

setup(
    name="neural-sync",  # Your package name
    version="0.1.0",  # Initial version
    author="Hasan Maqsood",
    author_email="hasanmaqsood2001@gmail.com",
    description="A library to standardize the usage of various machine learning models",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/HasanMaqsood8747/neuralsync.git",  # Optional GitHub repo URL
    packages=find_packages(),
    install_requires=[
        "torch==2.4.1",
        "transformers==4.44.2",
        "torchvision==0.19.1",
        "numpy==1.26.4",
        "pyannote.audio==3.3.1",
        "torchaudio==2.4.1",
        "accelerate==0.34.2",
        "openai==1.43.1",
        "huggingface-hub==0.23.4",
        "pydub==0.25.1",
        "SpeechRecognition==3.10.4",
        "Cython==3.0.11",
        "nemo_toolkit[all]==1.23.0",
        "diffusers==0.30.2",
        "sentencepiece==0.2.0",
        # Add others as needed
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10.12",  # Python version support
)
