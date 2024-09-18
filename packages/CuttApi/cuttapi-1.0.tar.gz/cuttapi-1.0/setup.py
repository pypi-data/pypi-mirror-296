from setuptools import setup, find_packages

setup(
    name='CuttApi',
    packages=find_packages(exclude=['docs']),
    version='1.0',
    license='MIT',
    description='One of the best ways of shortening URLs using Cuttly URL shortener just by entering your API key and seeing the rest that is done automatically by the Module',
    author='Devraj Therani',
    author_email='ttctlc96e@mozmail.com',
    url='https://github.com/devrajdevs/CuttApi',
    download_url='https://github.com/devrajdevs/CuttApi/archive/refs/tags/v1.0.tar.gz',
    keywords=['API', 'SIMPLE', 'URL', 'SHORTENER'],
    install_requires=[
        'requests',
        'urllib3',
        'pyperclip'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
