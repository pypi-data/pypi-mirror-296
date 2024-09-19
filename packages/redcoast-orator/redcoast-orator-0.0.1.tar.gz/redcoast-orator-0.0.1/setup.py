from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='redcoast-orator',
    version='0.0.1',
    packages=find_packages(),
    install_requires=[
        "torch",
        "transformers",
        "gradio",
        "pyMuPDF",
        "langchain==0.2.16",
        "langchain-chroma==0.1.3",
        "langchain-community==0.2.16",
        "langchain-core==0.2.38",
        "langchain-openai==0.1.23",
        "langgraph==0.2.19",
        "loguru",
        "GitPython"
    ],
    author="Redcoast AI Group",
    long_description=long_description,
    long_description_content_type="text/markdown"
)