from setuptools import setup


setup(
    name='brynq_sdk_factorial',
    version='0.3.0',
    description='Factorial wrapper from BrynQ',
    long_description='Factorial wrapper from BrynQ',
    author='BrynQ',
    author_email='support@brynq.com',
    packages=["brynq_sdk.factorial"],
    license='BrynQ License',
    install_requires=[
        'brynq-sdk-brynq>=1',
        'pandas>=2.2.0,<3.0.0',
    ],
    zip_safe=False,
)
