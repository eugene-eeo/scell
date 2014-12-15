import sys
from setuptools import setup
from setuptools.command.test import test as TestCommand


class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = ['--strict', '--verbose', '--tb=long', 'tests']
        self.test_suite = True

    def run_tests(self):
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='scell',
    version='0.2.1',
    description='simple wrapper atop select',
    license='MIT',
    author='Eugene Eeo',
    author_email='packwolf58@gmail.com',
    url='https://github.com/eugene-eeo/scell',
    keywords="selector io reactor",
    packages=['scell'],

    cmdclass={'test': PyTest},
    tests_require=['pytest'],
    extras_require={
        'testing': ['pytest'],
    },

    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
