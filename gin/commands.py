import os

import click

import gin.core as core

_APP = "gin"


@click.Group
def cli():
    pass


@cli.command(help="initialize gin for current user")
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


@cli.command(help="add gin repository")
@click.option("--alias", help='gin repo alias', required=True)
@click.option(
    "--type", "-t", "type_",
    help="type of gin repo",
    type=click.Choice(['local']),
    required=True
)
@click.option("--location", help="url for gin repo", required=True)
def add(alias, type_, location):
    core.add_repo(alias, type_, location, repo_path())


@cli.command(help="remove gin repository")
@click.option("--alias", help='gin repo alias', required=True)
def remove(alias):
    core.repo_remove(alias, repo_path())


@cli.command(help="list all gin repositories mapped for user")
def list():
    repos = core.get_repos(repo_path()).get('repos', {}).keys()
    click.echo(f"gin repos {list(repos)}")


@cli.command(help="get a gin from a repository alias")
@click.option("--alias", help='gin repo alias', required=True)
@click.option("--name", help='name of gin in alias', required=True)
def get(alias, name):
    core.get_gin(alias, name, repo_path(), bin_path())


@cli.command(help="search for gins available with current repositories")
@click.option("--alias", help='gin repo alias', required=True)
def search(alias):
    click.echo(f"Available gin in {alias}\n {core.list_gin(alias, repo_path())}")


def repo_path():
    return os.path.join(click.get_app_dir(_APP), "repos.json")


def bin_path():
    return os.path.join(click.get_app_dir(_APP), "bin")
