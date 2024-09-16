# setup.py
from setuptools import setup, find_packages

setup(
    name="uzpy",
    version="0.1",
    packages=find_packages(),
    install_requires=[],  # Agar kerak bo‘lsa qo‘shimcha kutubxonalarni bu yerga yozasiz
    description="o'zbek tilidagi puthon",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/qaxxorovgit/uzpy.git",  # GitHub sahifangiz manzili
    author="Qaxxorov DEVV",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
