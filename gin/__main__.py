#!/usr/bin/env python3

import json
from os.path import expanduser, join, isdir
import os
import stat

from gin.commands import cli

# def main():
#     print(gin_path_bin())
#     print(gin_path_repos())
#     print(get_repos())
#
#     add_repo("dev", "local", "~/tmp")
#     add_repo("dev2", "local", "~/tmp2")
#
#     list_gin("dev")
#     get_gin("dev", "hello")
#     get_gin("dev2", "hi")


if __name__ == "__main__":
    cli()
