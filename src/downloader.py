# -*- coding: utf-8 -*-

import os

import requests
import filetype


def download(url: str, file_path: str):
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(file_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)

    kind = filetype.guess(file_path)
    if kind:
        try:
            new_file_path = file_path + "." + kind.extension
            os.rename(file_path, new_file_path)
        except FileExistsError:
            pass

    return
