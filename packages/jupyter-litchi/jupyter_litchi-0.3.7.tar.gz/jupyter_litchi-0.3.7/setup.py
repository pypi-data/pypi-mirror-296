# from setuptools import setup
from pathlib import Path
from setuptools import find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

__import__("setuptools").setup(description="Litchi is a JupyterLab extension for AI Client",
                                     long_description=long_description,
                                     long_description_content_type='text/markdown',
                                     author="Mars Liu",
                                     author_email="mars.liu@outlook.com",
                                     keywords = [
                                             "jupyter",
                                             "jupyterlab",
                                             "jupyterlab-extension",
                                             "ai",
                                             "llm",
                                             "ollama",
                                             "openai",
                                             "agent"
                                         ],)
