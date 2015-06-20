import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

install_requires = [
    'djed.message',
    'djed.renderer',
    'pyramid',
    'pyramid_chameleon',
    'pytz',
]

tests_require = [
    'djed.testing',
]


setup(
    name='djed.form',
    version='0.0',
    description='Form generation library for Pyramid',
    long_description='\n\n'.join([README, CHANGES]),
    classifiers=[
        "Framework :: Pyramid",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: ISC License (ISCL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Topic :: Internet :: WWW/HTTP",
    ],
    author='Djed developers',
    author_email='djedproject@googlegroups.com',
    url='https://github.com/djedproject/djed.form',
    license='ISC License (ISCL)',
    keywords='web pyramid pylons',
    packages=['djed.form'],
    include_package_data=True,
    install_requires=install_requires,
    extras_require={
        'testing': tests_require,
    },
    test_suite='nose.collector',
)
