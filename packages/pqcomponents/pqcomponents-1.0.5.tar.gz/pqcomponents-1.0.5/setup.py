from setuptools import setup, find_packages

setup(
    name='pqcomponents',
    version='1.0.5',
    description='A custom PyQt5 widgets package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='JunKyu',
    author_email='jkjo0619@gmail.com',
    url='https://github.com/JunKyu-Cho/pqcomponents',
    packages=find_packages(),
    install_requires=[
       'PyQt5 >= 5.15.0'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
