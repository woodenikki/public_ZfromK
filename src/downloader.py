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

import requests
import filetype


# To improve this method someone could add downloading to a temp location
# then performing a mv to the correct location. this would allow easier
# resume handling... but if it is run with the delete flag then
# resuming is handled for us.
def download(url: str, file_path: str) -> int:
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

    return os.path.getsize(new_file_path)
