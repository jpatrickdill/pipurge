"""
PiPurge
=======

PiPurge is a tool to uninstall all packages installed, whether system level or virtualenv

``$ pipurge --help``
"""

from setuptools import setup


setup(
    name="pipurge",
    version="0.1.6",
    url="",
    license="MIT",
    author="Patrick Dill",
    author_email="jamespatrickdill@gmail.com",
    description="Uninstall every package. all of them.// now",
    long_description=__doc__,
    include_package_data=True,
    packages=["pipurge"],
    platforms="any",
    install_requires=["delegator.py", "Click", "colorama"],
    download_url="http://github.com/reshanie/pipurge/archive/master.tar.gz",
    classifiers=[
        # As from https://pypi.python.org/pypi?%3Aaction=list_classifiers
        # "Development Status :: 1 - Planning",
        # "Development Status :: 2 - Pre-Alpha",
        "Development Status :: 3 - Alpha",
        # "Development Status :: 4 - Beta",
        # "Development Status :: 5 - Production/Stable",
        # "Development Status :: 6 - Mature",
        # "Development Status :: 7 - Inactive",
        "Programming Language :: Python",
        # "Programming Language :: Python :: 2",
        # "Programming Language :: Python :: 2.3",
        # "Programming Language :: Python :: 2.4",
        # "Programming Language :: Python :: 2.5",
        # "Programming Language :: Python :: 2.6",
        # "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: System :: Systems Administration",
    ],
    entry_points="""
        [console_scripts]
            pipurge=pipurge:purge
    """
)
