from setuptools import setup, find_packages

with open("README.md", "r") as f:
    description = f.read()

setup(
    name='git-sherlock-tool',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        'ftfy==6.2.3',
        'pandas==2.2.2',
        'protobuf',
        'PyGithub==2.4.0',
        'python-dotenv==1.0.1',
        'Requests==2.32.3',
        'rich==13.8.0',
        'google.generativeai'
    ],
    entry_points={
        'console_scripts': [
            'git-sherlock=git_sherlock.main:main',
            'git-sherlock-interactive=git_sherlock.terminal:interactive_mode',
        ]
    },
    long_description=description,
    long_description_content_type="text/markdown",
)