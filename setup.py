"""spicy.feedback"""
from importlib import import_module
from setuptools import setup, find_packages


version = '1.0'
LONG_DESCRIPTION = """
spicy.feedback package
"""


def long_description():
    """Return long description from README.rst if it's present
    because it doesn't get installed."""
    try:
        return open('README.rst').read()
    except IOError:
        return LONG_DESCRIPTION


setup(
    name='spicy.feedback',
    version=version,
    author='Burtsev Alexander',
    author_email='eburus@gmail.com',
    description='Spicy Categories',
    license='BSD',
    keywords='django, cms',
    url='',

    packages=find_packages('src'),
    package_dir={
        '': 'src',
    },
    include_package_data=True,
    zip_safe=False,

    long_description=long_description(),

    namespace_packages=['spicy', ],
    install_requires=[
        'spicy>=1.1',
        'django-bitfield==1.6.4',
        'nexmomessage==dev'
    ],
    dependency_links=[
        'hg+http://hg.bramabrama.com/spicy#egg=spicy',
        'http://github.com/marcuz/libpynexmo/tarball/master#egg=nexmomessage-dev'
    ],

    classifiers=[
        'Framework :: Django',
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'License :: OSI Approved :: BSD License',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Programming Language :: Python :: 2.5',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ]
)
