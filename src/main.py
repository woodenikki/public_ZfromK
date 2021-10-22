#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from datetime import datetime

import click

from loguru import logger
from colorama import init, Fore

VERSION = Fore.YELLOW + "2.0.0" + Fore.RESET
VERSION_NAME = Fore.GREEN + "Brazen Beaver" + Fore.RESET
VERSION_ART = f"""
              ___
           .="   "=._.---.
         ."         c ' Y'`p
        /   ,       `.  w_/
        |   '-.   /     /
  _,..._|      )_-\ \_=.\\
 `-....-'`------)))`=-'"`'"  v{VERSION} {VERSION_NAME}
"""


@click.command()
@click.option(
    "-s",
    "--start",
    required=True,
    type=click.DateTime(["%m-%d-%Y"]),
    help="Starting date (MM-dd-yyyy)",
)
@click.option(
    "-e",
    "--end",
    required=True,
    type=click.DateTime(["%m-%d-%Y"]),
    help="Ending date (MM-dd-yyyy)",
)
@click.option("-d", "--delete", default=False, is_flag=True, help="Dry run (no delete)")
@click.option(
    "-p",
    "--path",
    default=".",
    type=click.Path(file_okay=False, writable=True, exists=True),
    help="Path to download files to",
)
@click.version_option(version=VERSION, message=f"%(version)s {VERSION_NAME}")
def main(
    start: datetime,
    end: datetime,
    delete: bool,
    path: str,
):

    print(VERSION_ART)

    if start >= end:
        logger.critical(f"Start date is after end date. Cant manipulate space time")
        sys.exit(1)


if __name__ == "__main__":
    init()
    main()
