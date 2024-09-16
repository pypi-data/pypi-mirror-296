from setuptools import setup, find_packages

setup(
    name="uzpy",
    version="0.4",
    packages=find_packages(),
    install_requires=["datetime"],  # List additional dependencies here if needed
    description="O'zbek tilidagi Python kutubxonasi",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",  # or "text/x-rst" if using reStructuredText
    author="Qaxxorov DEVV",
    url="https://www.youtube.com/@qaxxorovdevv",  # Consider adding a project URL
)
