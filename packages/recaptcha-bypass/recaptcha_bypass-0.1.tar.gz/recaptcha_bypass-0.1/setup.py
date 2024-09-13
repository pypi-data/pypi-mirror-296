from setuptools import setup, find_packages

setup(
    name='recaptcha-bypass',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
    ],
    description='A tool to bypass reCAPTCHA Enterprise v2 for educational purposes',
    author='Azrail',
    author_email='info@sociproviders.com',
    url='https://github.com/sociproviders/recaptcha-bypass',  # GitHub reposu veya diğer URL
)
