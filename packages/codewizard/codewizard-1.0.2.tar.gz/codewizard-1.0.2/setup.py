from setuptools import setup, find_packages

setup(
    name='codewizard',
    version='1.0.2',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'codewizard=codewizard.cli:main',
        ],
    },
    install_requires=[
        'click',
        'pyperclip',
        'pylint'
    ],
    author='Aman Saurav',
    author_email='amansaurav95@gmail.com',
    description='A powerful assistant toolkit for developers',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/oops-aman/codewizard',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
