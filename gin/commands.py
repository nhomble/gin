import os

import click

import gin.core as core

_APP = "gin"


@click.Group
def cli():
    pass


@cli.command()
def init():
    d = click.get_app_dir(_APP)
    bin_ = os.path.join(d, "bin")
    if not os.path.exists(bin_):
        os.makedirs(bin_)
    r = os.path.join(d, "repos.json")
    if not os.path.exists(r):
        with open(r, 'w') as f:
            f.write("{}")
    click.echo(f"Add to $PATH \"{bin_}")


@cli.command()
@click.option("--alias", help='gin repo alias', required=True)
@click.option(
    "--type", "-t", "type_",
    help="type of gin repo",
    type=click.Choice(['local']),
    required=True
)
@click.option("--location", help="url for gin repo", required=True)
def add_repo(alias, type_, location):
    core.add_repo(alias, type_, location, repo_path())


@cli.command()
@click.option("--alias", help='gin repo alias', required=True)
def repo_remove(alias):
    core.repo_remove(alias, repo_path())


@cli.command()
def list_repos():
    repos = core.get_repos(repo_path()).get('repos', {}).keys()
    click.echo(f"gin repos {list(repos)}")


@cli.command()
@click.option("--alias", help='gin repo alias', required=True)
@click.option("--name", help='name of gin in alias', required=True)
def get_gin(alias, name):
    core.get_gin(alias, name, repo_path(), bin_path())


@cli.command()
@click.option("--alias", help='gin repo alias', required=True)
def list_gin(alias):
    click.echo(f"Available gin in {alias}\n {core.list_gin(alias, repo_path())}")


def repo_path():
    return os.path.join(click.get_app_dir(_APP), "repos.json")


def bin_path():
    return os.path.join(click.get_app_dir(_APP), "bin")
