from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Intended Audience :: Science/Research',
    'Intended Audience :: Education',
    'Natural Language :: English',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
]

setup(
    name='kbtcal',
    version='1.3',
    description='This is a simple library that performs basic python arithmetic operations.',
    long_description=open('README.md').read() + '\n\n' +
    open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Kenneth Broni',
    author_email='kbroni123@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='calculator',
    packages=find_packages(),
    install_requires=['numpy>=1.21.0']
)
