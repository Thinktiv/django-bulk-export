from setuptools import setup, find_packages
 
setup(
    name='django-bulk-export',
    version=__import__('django_bulk_export').__version__,
    description='Django Bulk Export plugin using queues and asynchronus processing ',
    long_description=open('README.rst').read(),
    author='Amit Yadav',
    author_email='amit.yadav@joshlabs.in',
    url='http://github.com/Thinktiv/django-bulk-export',
    download_url='http://github.com/Thinktiv/django-bulk-export/downloads',
    license='BSD',
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
