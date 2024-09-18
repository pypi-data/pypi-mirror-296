# setup.py

from setuptools import setup, find_packages

setup(
    name='rakuten_do_dbt_processor',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[],
    entry_points={
        'console_scripts': [
            'rakuten_do_dbt_processor=rakuten_do_dbt_processor.processor:main',
        ],
    },
    author='Rakuten DO India',
    author_email='ankur.kumar@rakuten.com',
    description='A package to process dbt logs into Rakuten DO platform',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/rakuten_do_dbt_processor',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
