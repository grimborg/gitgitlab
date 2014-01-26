from setuptools import setup
import sys

setup(
    name='GitGitlab',
    version='1.0',
    description='gitlab for git',
    packages=['gitgitlab'],
    install_requires=map(str.strip, open('requirements.txt', 'r').readlines()),
    entry_points={'console_scripts': ['git-lab=gitgitlab.cli:git']}
)

