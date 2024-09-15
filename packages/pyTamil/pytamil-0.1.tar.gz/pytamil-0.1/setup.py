from setuptools import setup, find_packages

setup(
    name='pyTamil',           # Your package name
    version='0.1',               # Version
    packages=find_packages(),    # Automatically find packages in the current directory
    install_requires=["pydantic==2.9.1"],         # List dependencies here
    description='A simple example package',
    long_description=open('README.md').read(),  # README file as long description
    long_description_content_type='text/markdown',
    url='https://github.com/kamalkavin68/pyTamil',  # GitHub repo or other URL
    author='kamalkavin96',
    author_email='kamalkavin68@gmail.com',
    license='MIT',               # Choose a license
)
