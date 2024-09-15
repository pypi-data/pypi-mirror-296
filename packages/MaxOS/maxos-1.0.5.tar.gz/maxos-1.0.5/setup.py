from setuptools import setup, find_packages

setup(
    name='MaxOS',
    version='1.0.5',
    packages=find_packages(),
    description='MaxOS library',
    readme ='readme.md',
    install_requires=[
        'random',
        'time',
],
    author='fhghfhfhfh',
    author_email='maximdev@internet.ru',
    url='',  # Укажите ссылку на ваш репозиторий
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)