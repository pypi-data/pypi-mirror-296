from setuptools import setup, find_packages

setup(
    name='jw_pypi_sandbox',
    version='0.1.2',
    description='sb',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='JW',
    author_email='JW@code.com',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
