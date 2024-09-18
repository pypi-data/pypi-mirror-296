from setuptools import setup

setup(
    name='brynq_sdk_azure',
    version='1.1.1',
    description='Azure wrapper from BrynQ',
    long_description='Azure wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.azure"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'azure-storage-file-share>=12.6.0',
        'azure-storage-blob>=12.16.0',
        'msal==1.22.0'
    ],
    zip_safe=False,
)
