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

import re
import sys

import click
import delegator

requires = re.compile(r"Requires: (((, )?[\w\d\-._]+)+)")


def _dependencies(pkg):
    # returns direct dependencies of package

    pkg_info = delegator.run(["pip", "show", pkg], block=True).out

    requirements = requires.search(pkg_info)

    if requirements is None:
        return {pkg: {}}

    return requirements.group(1).split(", ")


def dependency_tree(pkg, out=None, ind=0):
    # returns dependency tree for package
    # ex:
    #     {
    #         "req_a": [
    #             {"sub_a": {}},
    #             {"sub_b": {
    #                 "sub_sub_a": {}
    #             }
    #         ],
    #         "req_b": {}
    #     }

    if out:
        out("{}Finding dependencies for {}...".format(" "*ind, pkg))

    requirements = _dependencies(pkg)

    tree = {}

    for req in requirements:
        if req == pkg:
            continue

        tree[req.lower()] = dependency_tree(req, out=out, ind=ind+2)

    return tree


def dependency_list(pkg, out=None):
    # returns list of recursive dependencies for package

    tree = dependency_tree(pkg, out=out)

    def prct(d):
        lst = []

        for k in d.keys():
            lst.append(k)

            for i in prct(d[k]):
                lst.append(i)

        return lst

    return prct(tree) + [pkg]


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
            "\nThere are {} packages to uninstall. Proceed?".format(click.style(str(len(packages)), fg="yellow"))):
        click.echo("Purge cancelled.")

        sys.exit(1)

    for p in packages:
        if ask:
            if not click.confirm("\nUninstall {} ?".format(click.style(p, fg="yellow"))):
                continue

        cmd = "pip uninstall {} -y".format(p)

        ran = delegator.run(cmd)

        click.secho(ran.out.rstrip("\n"), fg="red")

    click.secho("\nPurge complete!", fg="green")


if __name__ == "__main__":
    purge()
