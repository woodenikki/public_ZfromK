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
import re
import json

from datetime import datetime

from halo import Halo

from humanize import naturalsize, naturaltime

from KalturaClient import (
    KalturaConfiguration,
    KalturaClient,
)
from KalturaClient.exceptions import *
from KalturaClient.Plugins.Core import (
    KalturaSessionType,
    KalturaFilterPager,
    KalturaMediaEntry,
    KalturaMediaEntryFilter,
)

from .downloader import download

from typing import List, Dict, Any


class Client:

    # This is the tag id applied to all videos that were migrated from
    # zoom to kaltura. All videos with this id are tagged "zoom".
    __CATEGORY_ID__ = "159659192"

    def __init__(self, path: str) -> None:

        # This is the directory location that files will be written to
        # This location is initially tested to be both existant and
        # writable although this cannot be assumed.
        self.path = path

        # Total bytes downloaded during session
        self.__session_rx = 0

        config = KalturaConfiguration()

        # The prefix "__" marks a member attribute private in python by
        # performing "name mangling".
        #
        # Python has no clue what a private member is and has no mechanism
        # to protect anything with private or protected identifiers.
        # The reason is python thinks you are an adult and should be
        # able to blow your leg off if you so choose.
        #
        # A preceding __ will make the name _{Class_name}__{var_name}
        # So to access this variable outside of the class would look like:
        # ```python
        # object._Client__client.{METHOD}()
        # ````
        self.__client = KalturaClient(config)

        # This object generates a token that is used by the session
        # transparently and this is the only interaction that is
        # necessary.
        # Token and admin variables hidden in public version.
        ks = self.__client.session.start(
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
            KalturaSessionType.ADMIN,
            partnerId=0000000,      
            expiry=3600,
            privileges="appID:appName-appDomain",
        )

        self.__client.setKs(ks)

        # Before we exit the client wrapping class we can do a couple things
        # To make working with kaltura objects better. Like... actually printing
        # a human readable copy of objects! Boo Kaltura Boo!
        # No touchy touchy, this doesnt belong to you.
        # -----------------------------------------------------------+
        KalturaMediaEntry.__str__ = lambda self: str(vars(self))   # |
        KalturaMediaEntry.__repr__ = lambda self: str(vars(self))  # |
        # -----------------------------------------------------------+

    def search(
        self, start: datetime, end: datetime, page: int
    ) -> List[KalturaMediaEntry]:
        pager = KalturaFilterPager(pageSize=5, pageIndex=page)

        filter = KalturaMediaEntryFilter()
        filter.categoriesIdsMatchAnd = self.__CATEGORY_ID__
        filter.createdAtGreaterThanOrEqual = int(start.timestamp())
        filter.createdAtLessThanOrEqual = int(end.timestamp())

        return self.__client.media.list(filter, pager).objects

    def download(self, path: str, info: Dict[str, Any]):
        spinner = Halo(text=f'Downloading {info["name"]}', spinner="dots")
        spinner.start()

        file_path = os.path.join(
            path,
            info["userId"]
            + "_"
            + re.sub(
                "[^0-9a-zA-Z]+", "_", (str(datetime.fromtimestamp(info["createdAt"])))
            ),
        )
        try:
            os.mkdir(file_path)
        except FileExistsError:
            pass

        file_name = re.sub("[^0-9a-zA-Z]+", "_", info["name"])
        full_file_path = os.path.join(file_path, file_name)

        size = download(info["downloadUrl"], full_file_path)
        self.__session_rx += size

        with open(os.path.join(file_path, file_name + ".json"), "w") as f:
            json.dump(info, f)

        spinner.succeed(f"Downloaded: {info['name']} {naturalsize(size)}")

    def delete(self, info: Dict[str, Any]):
        spinner = Halo(text=f'Deleting {info["name"]}', spinner="dots")
        spinner.start()
        self.__client.media.delete(info["id"])

        spinner.succeed(f"Deleted {info['name']} successfully.")

    def stats(self):
        print("Total stats: " + naturalsize(self.__session_rx))
