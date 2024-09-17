from setuptools import setup, find_packages

with open("ReadMe.md", "r") as rm:
    pypidesc = rm.read()


setup(
    name='Email_Usage',
    version='1.2',
    packages=find_packages(),
    install_requires=[
        # no package required
    ],
    long_description=pypidesc,
    long_description_content_type='text/markdown'
)