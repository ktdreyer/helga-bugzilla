import re
from setuptools import setup, find_packages


def read_module_contents():
    with open('helga_bugzilla/__init__.py') as init:
        return init.read()


module_file = read_module_contents()
metadata = dict(re.findall(r"__([a-z]+)__\s*=\s*'([^']+)'", module_file))
version = metadata['version']


setup(
    name="helga-bugzilla",
    version=version,
    description=('bugzilla plugin for helga'),
    classifiers=['Development Status :: 4 - Beta',
                 'License :: OSI Approved :: MIT License',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python',
                 'Topic :: Software Development :: Bug Tracking',
                 ],
    keywords='irc bot bugzilla',
    author='ken dreyer',
    author_email='ktdreyer@ktdreyer.com',
    url='https://github.com/ktdreyer/helga-bugzilla',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'helga',
        'txbugzilla>=1.4.0',
    ],
    entry_points=dict(
        helga_plugins=[
            'bugzilla = helga_bugzilla:helga_bugzilla',
        ],
    ),
)
