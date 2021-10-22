# python -m src -s START -e END -p PATH --delete

#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  The MIT License (MIT)
#
# Copyright © 2020 Jacobsin.security@pm.me
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files
# (the “Software”), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
# Kaltura documentation available:
# https://developer.kaltura.com/api-docs/VPaaS-API-Getting-Started/introduction-kaltura-client-libraries.html


import os
import sys
import click
import logging

from .client import Client
from .parser import parse_time


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


VERSION = bcolors.WARNING + "2.0.0" + bcolors.ENDC
VERSION_NAME = bcolors.OKGREEN + "Brazen Beaver" + bcolors.ENDC
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
@click.version_option(version=VERSION, message=f"%(version)s {VERSION_NAME}")
@click.option("-s", "--start", required=True, help="Starting date (MM-dd-yyyy)")
@click.option("-e", "--end", required=True, help="Ending date (MM-dd-yyyy")
@click.option("-d", "--delete", default=False, is_flag=True, help="Dry run (no delete)")
@click.option(
    "-p",
    "--path",
    default=".",
    type=click.Path(file_okay=False, writable=True, exists=True),
    help="Path to download files to",
)
@click.option("-v", "--verbose", count=True)
def main(start, end, delete, path, verbose):
    """
    Entrypoint of the utilty to delete videos from Kaltura after
    downloading a copy.

    MIT license, DO NOT REMOVE LICENSE FROM SOURCE
    """

    print(VERSION_ART)

    # Max value for verbose is 4 anything higher just makes
    # stuff go weird
    if verbose > 4:
        logger.warning("Verbosity maximum is 4, setting verbosity to 4")
        verbose = 4

    # Loggers (typically) have levels that are (typically) enums
    # Thus their levels are a string representation of a value
    # in this case its integers in increments of 10.
    #
    # Critical 50
    # error    40 etc.
    #
    # So we take the highest level and subtract the verbosity level
    # multiplied by 10 to get the proper level! 
    logger.setLevel(50 - (verbose * 10))

    start = parse_time(start)
    end = parse_time(end)

    if start >= end:
        logger.critical(f"Start date is after end date. Cant manipulate space time")
        sys.exit(1)

    logger.info(f"Start: {start} -> End: {end}")

    # This is our client object that we will use for every interaction with
    # Kaltura, like our search and delete functions.
    KalturaClient = Client(os.path.abspath(path))

    page = 1
    while True:
        # Chunk the results list and parse them in paged sets
        result = KalturaClient.search(start, end, page)
        page += 1

        # if the set of results returned is an empty set then we have
        # exhausted all media that is found in the supplied date range.
        if len(result) == 0:
            break

        # Download and delete here
        for item in result:
            logger.info("Item:", item.name, "by", item.userId)

            # dictionary comprehension to get only object in the class whose underlying type is
            # a str, int, list or dict. No objects please!
            info = {
                key: item.__dict__[key]
                for key in item.__dict__
                if type(item.__dict__[key]) in [int, str, list, dict]
            }

            # comment this if you don't want to download!!
            # KalturaClient.download(path, info)

            if delete:
                KalturaClient.delete(info)

        KalturaClient.stats()


if __name__ == "__main__":
    logger = logging.getLogger(__name__)

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(levelname)s - %(message)s"))
    logger.addHandler(handler)

    main()
