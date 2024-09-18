from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asker-cli',
    version='0.2.0',
    description='A CLI tool for getting quick answers to programming questions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Benyamin Damircheli',
    url='https://github.com/BenyaminDamircheli/Asker',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'ask=asker.ask:main',
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)