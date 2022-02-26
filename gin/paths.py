import os

import click

from gin import APP_NAME


def repo_path():
    return os.path.join(click.get_app_dir(APP_NAME), "repos.json")


def bin_path():
    return os.path.join(click.get_app_dir(APP_NAME), "bin")


def var_path():
    return os.path.join(click.get_app_dir(APP_NAME), "var")
