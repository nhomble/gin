import click


class AliasDoesNotExist(click.UsageError):
    def __init__(self, alias):
        super().__init__(f"alias={alias} does not exist")


class AliasConflict(click.UsageError):
    def __init__(self, alias):
        super().__init__(f"alias={alias} already exists")
