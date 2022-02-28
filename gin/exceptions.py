import click


class AliasDoesNotExist(click.UsageError):
    def __init__(self, alias):
        super(f"alias={alias} already exists!")
