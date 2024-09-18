from setuptools import setup, find_packages

setup(
    name='PyTorchLabFlow',
    version='0.1.6',
    package_dir={'': 'src'},  # Use 'src' as the root for packages
    packages=find_packages(where='src'),
    install_requires=[
        'torch',
        'librosa',
        'pandas',
        'tqdm'
    ],
    author='BBEK-Anand',
    author_email='',
    description='Framework for managing Torch models/experiments',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/BBEK-Anand/PyTorchLabFlow',
    license="MIT",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
