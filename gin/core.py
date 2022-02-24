import json
import os
import stat
from os.path import isdir, join, expanduser

import click


def get_repos(repo_path):
    with open(repo_path, 'r') as f:
        s = f.read()
        if s == "":
            return {"repos": {}}
        return json.loads(s)


def get_gin(alias, name, repo_path, bin_path):
    meta = get_repos(repo_path)['repos'].get(alias, None)
    if meta is None:
        fail("no alias " + alias)
    if meta['type'] == "local":
        path = expanduser(meta['location'])
        path = join(path, name)
        dest = join(bin_path, f"@gin:{alias}:{name}")
        with open(path, 'r') as frm:
            with open(dest, 'w') as to:
                to.write(frm.read())
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


def repo_remove(alias, repo_path):
    d = get_repos(repo_path)
    with open(repo_path, 'w') as f:
        repos = d.get("repos", {})
        if alias in repos:
            del repos[alias]
        d['repos'] = repos

        json.dump(d, f)


def add_repo(alias, repo_type, location, repo_path):
    d = get_repos(repo_path)
    with open(repo_path, 'w') as f:
        repos = d.get("repos", {})
        if alias in repos:
            raise click.UsageError(
                f"alias={alias} already exists - choose a different name or remove the existing repo")
        repo = repos.get(alias, {})
        repo['type'] = repo_type
        repo['location'] = location
        repos[alias] = repo
        d['repos'] = repos

        json.dump(d, f)
