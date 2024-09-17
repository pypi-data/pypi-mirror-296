from setuptools import setup

setup(
    name='wrm3_term_colors',  # The name you chose, check it's unique on PyPI
    version='0.1.2',
    packages={'wrm3_term_colors': ['*.py']},
    install_requires=[],  # List any dependencies here
    author='WRM3',
    author_email='wrmartel3@gmail.com',
    description='A terminal printing library that adds more color options.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/wrm3/wrm3_term_colors.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
