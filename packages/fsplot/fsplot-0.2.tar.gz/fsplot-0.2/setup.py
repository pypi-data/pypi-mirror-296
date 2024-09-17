from setuptools import setup, find_packages

setup(
    name='fsplot',
    version='0.2',
    description='`fsplot` is a Python library for lightweight visualization of financial market data using SVG.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Ryan L.',
    author_email='rylu.lubis@gmail.com',
    url='https://github.com/ryanllu/fs-plot',  # Replace with your actual repository URL
    packages=find_packages(),
    install_requires=[
        'svgwrite>=1.4.1',
        'numpy>=1.21.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
