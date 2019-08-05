import os
from setuptools import setup, find_packages
from DockerWestHosts.version import __version__


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="DockerWest Hosts Updater",
    version=__version__,
    author="Ike Devolder",
    author_email="ike.devolder@gmail.com",
    description="Automatically update /etc/hosts for your running containers",
    license="GPLv3",
    keywords="docker development events",
    url="https://dockerwest.gitlab.io",
    packages=find_packages(),
    scripts=['dockerwest-hosts-updater'],
    install_requires=[],
    python_requires='>3.4',
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
    ],
)
