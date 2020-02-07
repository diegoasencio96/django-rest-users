from setuptools import setup

setup(
    name='django-rest-users',
    packages=['django-rest-users'],
    version='0.0.1',
    description='Basic Endpoints REST API for User Models',
    author='Diego A Asencio C',
    license='MIT',
    author_email='diegoasencio96@gmail.com',
    url='https://github.com/diegoasencio96/django-rest-users/',
    download_url='https://github.com/diegoasencio96/django-rest-users/releases/tag/0.0.1',
    keywords=['django-rest-users', 'rest', 'users'],
    include_package_data=True,
    zip_safe=True,
    py_modules=['django-rest-users'],
    install_requires=[
        'djangorestframework',
    ],
)