import json
import os
import stat
from os.path import isdir, join, expanduser

import click
import requests

from gin.exceptions import AliasDoesNotExist
from gin.paths import repo_path, var_path, bin_path


def init():
    if not os.path.exists(bin_path()):
        os.makedirs(bin_path())
    if not os.path.exists(repo_path()):
        with open(repo_path(), 'w') as f:
            f.write("{}")
    if not os.path.exists(var_path()):
        os.makedirs(var_path())


def sh(cmd):
    print(cmd)
    os.popen(cmd).close()


def sync_repo(alias):
    sh(f"git -C \"{os.path.join(var_path(), alias)}\" pull")


def get_repos():
    with open(repo_path(), 'r') as f:
        s = f.read()
        if s == "":
            return {"repos": {}}
        return json.loads(s)


def get_gin(alias, name):
    if not repo_exists(alias):
        raise AliasDoesNotExist(alias)

    dest = ""

    st = os.stat(dest)
    os.chmod(dest, st.st_mode | stat.S_IXUSR | stat.S_IXOTH)


def list_gin(alias):
    if not repo_exists(alias):
        raise AliasDoesNotExist(alias)
    sync_repo(alias)
    p = os.path.join(var_path(), alias)
    return [f for f in os.listdir(p) if not isdir(join(p, f))]


def repo_remove(alias):
    if not repo_exists(alias):
        raise AliasDoesNotExist(alias)
    dest = os.path.join(var_path(), alias)
    sh(f"rm -rf \"{dest}\"")


def repo_list():
    return [f for f in os.listdir(var_path()) if isdir(join(var_path(), f))]


def repo_exists(alias):
    return os.path.exists(os.path.join(var_path(), alias))


def add_repo(alias, location):
    if repo_exists(alias):
        raise AliasDoesNotExist(alias)
    dest = os.path.join(var_path(), alias)
    sh(f"git clone \"{location}\" \"{dest}\"")
