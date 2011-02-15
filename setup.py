from setuptools import setup, find_packages

setup(
    name='panya-music',
    version='0.0.4',
    description='Panya music app.',
    long_description = open('README.rst', 'r').read(),
    author='Praekelt Foundation',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://github.com/praekelt/panya-music',
    packages = find_packages(),
    install_requires = [
        'django-ckeditor',
        'django-preferences',
        'panya',
        'pylast',
    ],
    include_package_data=True,
    classifiers = [
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
)
