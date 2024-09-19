from setuptools import setup, find_packages

setup(
    name='odyagent2409',
    version='0.1.1',
    description='Python module with a CLI exposing various agents prototyped workflow/actions',
    author='Your Name',
    author_email='jgi@jgwill.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=[
        'langchain',
        'langchain_community',
        'langchain_openai',
        'langchain-experimental',
    ],
    entry_points={
        'console_scripts': [
            'oxiv = cli_jgmarxiv:main',
        ],
    },
)
