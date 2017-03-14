"""spicy.feedback"""
from setuptools import setup, find_packages


version = '1.1.0'
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
    author='BramaBrama Ltd.',
    author_email='help@spicycms.com',
    description='Spicy feedback',
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
        'django-bitfield==1.6.4',
        'Django<=1.5.12',

        # Deprecated
        # comment it because PIP deprecate --process-dependency-links feature
        # and ignore dependency links by default.
        # Put nexmomessage to your requirements.txt file        
        #'nexmomessage==0.0.1'
        
    ],

    #dependency_links=[
    #    'http://github.com/marcuz/libpynexmo/tarball/master#egg=nexmomessage-0.0.1',
    #],

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
