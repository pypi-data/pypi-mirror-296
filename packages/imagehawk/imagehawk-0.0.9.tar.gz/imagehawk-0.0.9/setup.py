from setuptools import setup, find_packages


setup(
    name='imagehawk',
    version='0.0.9',
    packages=find_packages(exclude=["setup.py"]),
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
    author_email='junaidkernel@gmail.com',
    url='',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
