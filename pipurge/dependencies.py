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

# Generates dependency tree for Python package.

import delegator
import re

requires = re.compile(r"Requires: (([\w\d\-_.]+)(, [\w\d-]+)*)")


def _dependencies(pkg):
    # returns direct dependencies of package

    pkg_info = delegator.run(["pip", "show", pkg], block=True).out

    requirements = requires.search(pkg_info)

    if requirements is None:
        return {pkg: {}}

    return requirements.group(1).split(", ")


def dependency_tree(pkg, out=None):
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
        out("Finding dependencies for {} ...".format(pkg))

    requirements = _dependencies(pkg)

    tree = {}

    for req in requirements:
        if req == pkg:
            continue

        tree[req] = dependency_tree(req, out=out)

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
