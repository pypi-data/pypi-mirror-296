from setuptools import setup, find_packages

setup(
    name='openvlm',  # The name of your package
    version='0.0.1',  # Initial release version
    description='Self-hosting VLMs made easy',
    long_description=open('README.md').read(),  # For PyPI, use the README for the long description
    long_description_content_type='text/markdown',  # Tell PyPI to render it as Markdown
    author='Sean Sheng',
    author_email='ssheng@bentoml.com',
    url='https://github.com/bentoml/OpenVLM',
    license='MIT',  # Or whatever license you choose
    packages=find_packages(),  # Automatically find package directories
    install_requires=[],  # List any package dependencies here
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
