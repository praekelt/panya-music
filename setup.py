from setuptools import setup, find_packages

setup(
    name='django-music',
    version='dev',
    description='Django music app.',
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    url='https://github.com/praekelt/django-music',
    packages = find_packages(),
    include_package_data=True,
)
