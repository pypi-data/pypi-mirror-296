from setuptools import setup, find_packages

setup(
    name='cellular-automata-game-of-life',
    version='1.0.3',
    description='A modern implementation of Conway\'s Game of Life with interactive features.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Shiv Shankar Singh',
    author_email='shivshankarsingh.py@gmail.com',
    url='https://github.com/shiv3679/Cellular-Automata',  # Your GitHub repo link
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'matplotlib',
    ],
    entry_points={
        'console_scripts': [
            'conways-game=conways_game_of_life.cli:main',  # Entry point for your CLI
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
