from setuptools import setup, find_packages

setup(
    name='drcode-python',
    version='1.0.2',
    packages=find_packages(),
    install_requires=[
        'sentry-sdk>=2.0.0', 
    ],
    author='Ashutosh Renu',
    author_email='ashutosh@airia.in',
    description='This package provides a comprehensive solution for integrating advanced error tracking and performance monitoring into your application. It offers a set of powerful configuration options to tailor the integration to your specific needs.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/airia-in/DrCode-python-package',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    python_requires='>=3.6',  # Specify minimum Python version
    project_urls={  # Additional metadata
        'Documentation': 'https://github.com/airia-in/DrCode-python-package#readme',
        'Source': 'https://github.com/airia-in/DrCode-python-package',
    },
)
