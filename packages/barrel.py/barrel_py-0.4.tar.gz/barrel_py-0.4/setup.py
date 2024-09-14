from setuptools import setup, find_packages

setup(
    name='barrel.py',  # This is the name on PyPI
    version='0.4',
    packages=find_packages(include=['barrels', 'barrels.*']),  # Use 'barrels' as the import name
    install_requires=[
        'discord.py>=2.0.0',
        'colorama>=0.4.0',
        'aiohttp>=3.8.0',
        # `logging` is part of the Python standard library and does not need to be included
    ],
    entry_points={
        'console_scripts': [
            'barrel=barrels.main:main',  # Adjust this if main function is elsewhere
        ],
    },
    python_requires='>=3.7',
    author='Bytehook',
    author_email='frankkostine@gmail.com',
    description='A simple Discord bot package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    license='MIT',  # Choose an appropriate license
)
