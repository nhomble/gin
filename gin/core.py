import json
import os
import stat
from os.path import isdir, join, expanduser

import click
import requests

from gin.paths import repo_path, var_path


def sh(cmd):
    print(cmd)
    os.popen(cmd).close()


def sync_repo(alias, repo_path, var_path):
    d = get_repos(repo_path)
    data = d["repos"][alias]
    dest = os.path.join(var_path, alias)

    sh(f"git -C pull \"{dest}\"")


def get_repos():
    with open(repo_path(), 'r') as f:
        s = f.read()
        if s == "":
            return {"repos": {}}
        return json.loads(s)


def get_gin(alias, name, repo_path, bin_path):
    meta = get_repos(repo_path)['repos'].get(alias, None)
    dest = join(bin_path, f"@gin:{alias}:{name}")
    if meta is None:
        fail("no alias " + alias)
    if meta['type'] == "local":
        path = expanduser(meta['location'])
        path = join(path, name)

        with open(path, 'r') as frm:
            with open(dest, 'w') as to:
                to.write(frm.read())

    elif meta['type'] == 'http':
        r = requests.get(meta['location'], allow_redirects=True)
        open(dest, 'wb').write(r.content)

    st = os.stat(dest)
    os.chmod(dest, st.st_mode | stat.S_IXUSR | stat.S_IXOTH)


def fail(msg):
    print(msg)
    exit(1)


def list_gin(alias, repo_path):
    meta = get_repos(repo_path)['repos'].get(alias, None)
    if meta is None:
        fail("no alias " + alias)
    if meta['type'] == "local":
        path = expanduser(meta['location'])
        files = os.listdir(path)
        return [f for f in files if not isdir(join(path, f))]


def repo_remove(alias):
    if not repo_exists(alias):
        raise click.UsageError(f"alias={alias} does not exist!")
    dest = os.path.join(var_path(), alias)
    sh(f"rm -rf \"{dest}\"")


def repo_list():
    return [f for f in os.listdir(var_path()) if isdir(join(var_path(), f))]


def repo_exists(alias):
    return os.path.exists(os.path.join(var_path(), alias))


def add_repo(alias, location):
    if repo_exists(alias):
        raise click.UsageError(f"alias={alias} already exists!")
    dest = os.path.join(var_path(), alias)
    sh(f"git clone \"{location}\" \"{dest}\"")
