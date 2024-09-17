from setuptools import setup, find_packages

with open("README.md", "r") as file:
    description = file.read()

setup(
    name='simple-telegram-api',
    version='0.2.0',
    author='Ahmet Burhan Kayalı',
    author_email='ahmetburhan1703@gmail.com',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    description='A simple telegram bot api',
    long_description=description,
    long_description_content_type="text/markdown",
    keywords=['python', 'telegram', 'telegram api', 'bot api', 'bot', 'api'],
)
