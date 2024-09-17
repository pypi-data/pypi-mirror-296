from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='wrm3_term_colors',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        # Add your dependencies here, e.g.,
        # 'colorama>=0.4.4',
    ],
    author='WRM3',
    author_email='wrmartel3@gmail.com',
    description='A terminal printing library that adds more color options.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/wrm3/wrm3_term_colors',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
