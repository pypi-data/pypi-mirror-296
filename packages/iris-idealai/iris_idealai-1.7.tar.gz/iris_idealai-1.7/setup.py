from setuptools import setup, find_packages

setup(
    name="iris_idealai",
    version="1.7",
    packages=["iris_idealai"],
    install_requires=[
        "google-generativeai",
        "pillow", 
        "requests", 
        "python-dotenv", 
    ],
    description="A module to interact with Iris that is developed by Idea AI",
    author="Ideal AI",
    author_email="",
    url="https://idealai.netlify.app",
)