#!/usr/bin/env python
from __future__ import print_function

import os
import subprocess
import sys

import argparse

DESCRIPTION = "Homebrew/linuxbrew extension using platform-brew to install and source Galaxy Tool Shed packages."
DEFAULT_TOOLSHED_TAP_USER = "galaxyproject"
VERBOSE = False


def main():
    global VERBOSE
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("--brew", help="Path to Homebrew/linuxbrew 'brew' executable to target", default="brew")
    actions = ["shed-install", "shed-uninstall", "shed-env"]
    action = __action(sys)
    if not action:
        parser.add_argument('action', metavar='action', help="Versioned action to perform.", choices=actions)
    parser.add_argument('owner', metavar='owner', help="Tool Shed owner of package.")
    parser.add_argument('name', metavar='name', help="Tool Shed repository name of package.")
    parser.add_argument('--toolshed', help="Tool Shed tap (defaults to galaxyproject/toolshed).", default="toolshed")
    parser.add_argument('--verbose', action='store_true', help="Verbose output")
    parser.add_argument('restargs', nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if "/" not in args.toolshed:
        args.toolshed = "%s/%s" % (DEFAULT_TOOLSHED_TAP_USER, args.toolshed)
    __ensure_shed_tapped(args.brew, args.toolshed)
    if args.verbose:
        VERBOSE = True

    recipe_name = Package.from_args(args).recipe_name
    if not action:
        action = args.action
    cmds = [args.brew]
    if action == "shed-install":
        cmds.extend(["vinstall", recipe_name, "1.0"])
    elif action == "shed-uninstall":
        cmds.extend(["vuninstall", recipe_name, "1.0"])
    elif action == "shed-env":
        cmds.extend(["env", recipe_name, "1.0"])
    execute(cmds, stdout=None, stderr=None)


def __action(sys):
    script_name = os.path.basename(sys.argv[0])
    if script_name.startswith("brew-"):
        return script_name[len("brew-"):]
    else:
        return None


class Package(object):

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
    
    @staticmethod
    def from_args(args):
        # TODO: handle optional package name and version if package
        # repository declares multiple packages.
        owner = args.owner
        name = args.name
        return Package(owner=owner, name=name)

    @property
    def recipe_name(self):
        return build_recipe_name(None, None, self.owner, self.name)


def __ensure_shed_tapped(brew, toolshed_tap):
    execute(["/bin/sh", "-c", "%s tap %s || true" % (brew, toolshed_tap)])


# Take from Galaxy dependency resolver.
def build_recipe_name(package_name, package_version, repository_owner, repository_name):
    owner = repository_owner.replace("-", "")
    name = repository_name
    name = name.replace("_", "").replace("-", "")
    base = "%s_%s" % (owner, name)
    return base


# Next two defs (exeucte, CommandLineException copied and pasted
# from platform brew.
def execute(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=None):
    subprocess_kwds = dict(
        shell=False,
        stdout=stdout,
        stderr=stderr,
    )
    if env:
        subprocess_kwds["env"] = env
    p = subprocess.Popen(cmds, **subprocess_kwds)
    #log = p.stdout.read()
    global VERBOSE
    stdout, stderr = p.communicate()
    if p.returncode != 0:
        raise CommandLineException(" ".join(cmds), stdout, stderr)
    if VERBOSE:
        print(stdout)
    return stdout


class CommandLineException(Exception):

    def __init__(self, command, stdout, stderr):
        self.command = command
        self.stdout = stdout
        self.stderr = stderr
        self.message = ("Failed to execute command-line %s, stderr was:\n"
                        "-------->>begin stderr<<--------\n"
                        "%s\n"
                        "-------->>end stderr<<--------\n"
                        "-------->>begin stdout<<--------\n"
                        "%s\n"
                        "-------->>end stdout<<--------\n"
                        ) % (command, stderr, stdout)

    def __str__(self):
        return self.message


if __name__ == "__main__":
    main()
