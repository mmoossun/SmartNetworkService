from setuptools import setup, find_packages

setup(
    name='chatBot',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'langchain',
        'openai',
        'tiktoken',
        'chromadb',
        'unstructured',
    ],
)