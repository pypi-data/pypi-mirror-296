from setuptools import setup, find_packages

setup(
    name='horus-ai-labs-sdk',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests'
    ],
    author='Horus AI Labs',
    author_email='horusailabs@gmail.com',
    description='Python SDK for Horus AI Labs',
    url='https://github.com/Video-Search-AI/horus_ai_labs_sdk',
    keywords='sdk, video processing',
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires=">=3.6",
)
