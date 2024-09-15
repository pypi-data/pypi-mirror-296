from setuptools import setup, find_packages

setup(
    name='imagehawk',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        "qdrant-client==1.11.1",
        "transformers==4.44.2",
        "requests==2.32.3",
        "torch==2.4.1"
    ],
    description='A package for text to image search using embeddings',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Junaid Bashir',
    author_email='',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
