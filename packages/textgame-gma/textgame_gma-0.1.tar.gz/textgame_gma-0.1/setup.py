from setuptools import setup, find_packages

setup(
    name='textgame-gma',
    version='0.1',
    packages=find_packages(),
    description='A library for creating text-based games.',
    long_description=open('C:/Users/User/Documents/joao/textgame/README.md').read(),
    long_description_content_type='text/markdown',
    author='peg',
    author_email='jpg01153@gmail.com',
    url='https://github.com/bruno1994122/textgame',  # Substitua pelo link do seu repositório
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
