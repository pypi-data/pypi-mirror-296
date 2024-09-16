from setuptools import setup


setup(
    name='brynq_sdk_sage',
    version='0.0.1',
    description='Sage 50 UK on premise wrapper from BrynQ',
    long_description='Sage 50 UK on premise wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.sage"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=2.2.0,<3.0.0',
    ],
    zip_safe=False,
)
