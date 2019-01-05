"""
Copyright (c) 2017 Patrick Dill

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys

import click
import delegator

from dependencies import dependency_list


def is_venv():
    return (hasattr(sys, 'real_prefix') or
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))


# necessary for pipurge
DONT_UNINSTALL = [
    "pipurge",
    "click",
    "delegator.py", "pexpect", "ptyprocess",
    "colorama",
    "pipenv",  # pipenv is holy
    "virtaulenv",
    "virtualenv-clone"
]


@click.command()
@click.option("--ask", "-a", is_flag=True, default=False, help="Asks if each individual package should be uninstalled.")
@click.option("--keep", "-k", type=str, help="Comma delimited list of packages to keep installed.")
def purge(ask, keep):
    """Uninstalls all packages installed with pip."""

    # show warning if not in virtualenv
    if not is_venv():
        if not click.confirm(click.style("There is no active virtualenv, meaning this will uninstall all system level"
                                         " packages. Proceed?", fg="red")):
            sys.exit(1)

    frozen = delegator.run("pip freeze").out

    to_keep = DONT_UNINSTALL

    if keep:
        for pkg in keep.split(","):
            requirements = dependency_list(pkg, out=click.echo)

            to_keep = to_keep + requirements

    # ignore packages in DONT_UNINSTALL
    packages = []
    for package in frozen.split():
        p = package.split("==")[0].lower()
        if p not in to_keep:
            packages.append(p)

    if not click.confirm(
            "There are {} packages to uninstall. Proceed?".format(click.style(str(len(packages)), fg="yellow"))):
        sys.exit(1)

    click.echo()

    for p in packages:
        if ask:
            if not click.confirm("Uninstall {} ?".format(click.style(p, fg="yellow"))):
                continue

        cmd = "pip uninstall {} -y".format(p)

        ran = delegator.run(cmd)

        click.secho(ran.out, fg="red")


if __name__ == "__main__":
    purge()
