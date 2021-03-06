import os

import click

import gin.core as core
from gin.log import LOG
from gin.paths import var_path, repo_path, bin_path


@click.Group
def cli():
    pass


@cli.command(help="initialize gin for current user")
def init(interactive=False):
    """
    initializes the directory structure for gin for the current user
    :return:
    """
    LOG.info("asd")
    core.init()
    click.echo(f"Add to $PATH \"{bin_path()}\"")


@cli.command(help="add gin repository")
@click.option("--alias", help='gin repo alias', required=True)
@click.option("--location", help="url for gin repo", required=True)
def add(alias, location):
    core.init()
    core.add_repo(alias, location)


@cli.command(help="remove gin repository")
@click.option("--alias", help='gin repo alias', required=True)
def remove(alias):
    core.init()
    core.repo_remove(alias)


@cli.command(help="list all gin repositories mapped for user")
def list():
    core.init()
    repos = core.repo_list()
    msg = "\n".join(repos)
    click.echo(f"gin repos\n{msg}")


@cli.command(help="get a gin from a repository alias")
@click.option("--alias", help='gin repo alias', required=True)
@click.option("--name", help='name of gin in alias', required=True)
def get(alias, name):
    core.init()
    core.get_gin(alias, name)


@cli.command(help="search for gins available with current repositories")
@click.option("--alias", help='gin repo alias', required=True)
def search(alias):
    core.init()
    click.echo(f"Available gin in {alias}\n {core.list_gin(alias)}")
