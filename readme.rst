Pipurge
=======

.. image:: https://img.shields.io/pypi/v/pipurge.svg
    :target: https://pypi.python.org/pypi/pipurge


**Pipurge** is a tool that allows you to quickly uninstall Python packages, at system level or in a
virtualenv.

Usage
~~~~~

Basic usage:

.. code-block:: console

    $ pipurge

      There are 23 packages to uninstall. Proceed? [y/N]: y

      Uninstalling aiodns-1.1.1:
        Successfully uninstalled aiodns-1.1.1

      Uninstalling aiohttp-2.2.5:
        Successfully uninstalled aiohttp-2.2.5

      Uninstalling async-timeout-2.0.0:
        Successfully uninstalled async-timeout-2.0.0

      Uninstalling certifi-2018.11.29:
        Successfully uninstalled certifi-2018.11.29

      ...

You can also use the **--keep** option to specify certain packages to keep installed.
Pipurge will also keep the dependencies of the packages you specify so they stay working.

If you'd like further control over the process, use the **--ask** option and Pipurge
will ask you whether to uninstall each package that's left.

.. code-block:: console

    $ pipurge --keep requests,flask --ask

      Finding dependencies for requests...
        Finding dependencies for certifi...
        Finding dependencies for chardet...
        Finding dependencies for idna...
        Finding dependencies for urllib3...
      Finding dependencies for flask...
        Finding dependencies for Werkzeug...
        Finding dependencies for Jinja2...
          Finding dependencies for MarkupSafe...
        Finding dependencies for itsdangerous...
        Finding dependencies for click...

      There are 3 packages to uninstall. Proceed? [y/N]: y

      Uninstall bleach ? [y/N]: y
      Uninstalling bleach-3.0.2:
        Successfully uninstalled bleach-3.0.2

      Uninstall docutils ? [y/N]: n

      Uninstall faste ? [y/N]: y
      Uninstalling faste-0.2.5:
        Successfully uninstalled faste-0.2.5

      Purge complete!


