# -*- coding: utf-8 -*-

import os
import re
import json

from datetime import datetime

from halo import Halo

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


class Kaltura:
    def __init__(self, path: str):
        # Tag id applied to all videos magrated from Zoom
        self.__CATEGORY_ID = "159659192"

        # Path to download videos to
        self.path = path

        config = KalturaConfiguration()

        self.__client = KalturaClient(config)

        # Kaltura doesn't like printing human readable things.
        # No touchy touchy, this doesnt belong to you.
        # -----------------------------------------------------------+
        KalturaMediaEntry.__str__ = lambda self: str(vars(self))  # |
        KalturaMediaEntry.__repr__ = lambda self: str(vars(self))  # |
        # -----------------------------------------------------------+

    # Search Kaltura; retrieve videos within user's daterange that have the Zoom ID tag
    def search(
        self, start: datetime, end: datetime, page: int
    ) -> List[KalturaMediaEntry]:
        pager = KalturaFilterPager(pageSize=5, pageIndex=page)

        filter = KalturaMediaEntryFilter()
        filter.categoriesIdsMatchAnd = self.__CATEGORY_ID
        filter.createdAtGreaterThanOrEqual = int(start.timestamp())
        filter.createdAtLessThanOrEqual = int(end.timestamp())

        return self.__client.media.list(filter, pager).objects


    # Delete a video from Kaltura
    def delete(self, info: Dict[str, Any]):
        spinner = Halo(text=f'Deleting {info["name"]}', spinner="dots")
        spinner.start()
        self.__client.media.delete(info["id"])

        spinner.succeed(f"Deleted {info['name']} successfully.")

    # Download the video to our file path. Replace any nasty characters with '_'
    def download(self, path: str, info: Dict[str, Any]):
        spinner = Halo(text=f'Downloading {info["name"]}', spinner="dots")
        spinner.start()

        _regex = "[^0-9a-zA-Z]+"

        _creation_time = str(datetime.fromtimestamp(info["createdAt"]))

        dir_path = info["userId"] + "_" + re.sub(_regex, "_", _creation_time)

        full_dir_path = os.path.join(path, dir_path)

        if not os.path.exists(full_dir_path):
            os.mkdir(full_dir_path)

        file_name = re.sub(_regex, "_", info["name"])
        file_path = os.path.join(full_dir_path, file_name)

        download(info["downloadUrl"], file_path)

        with open(os.path.join(full_dir_path, file_name + ".json"), "w") as f:
            json.dump(info, f)

        spinner.succeed(f"Downloaded: {info['name']}")
