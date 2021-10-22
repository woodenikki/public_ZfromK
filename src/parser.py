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

import sys
import logging

from datetime import datetime

logger = logging.getLogger(__name__)


# This function when given a string that represents a datetime object
# of the format mm-dd-YYYY.
#
# We use the datetime object to ensure the user doesnt give us bad
# input and do horrible things to our search method in the client class
def parse_time(dt: str) -> datetime:
    try:
        logger.info(f"Parsing time {dt}")
        return datetime.strptime(dt, "%m-%d-%Y")
    except ValueError:
        logger.critical(f"Failed to parse provided datetime {dt}")
        sys.exit(1)
