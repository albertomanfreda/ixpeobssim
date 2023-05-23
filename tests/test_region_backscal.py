#!/usr/bin/env python
#
# Copyright (C) 2021, the ixpeobssim team.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""Unit test for the BACKSCAL keyword support in region-selected sources.
"""

from __future__ import print_function, division

import unittest
import sys
import os

import numpy
from ixpeobssim.core import pipeline
from ixpeobssim.evt.event import xEventFile
from ixpeobssim import IXPEOBSSIM_TEST_DATA
from ixpeobssim import IXPEOBSSIM_CONFIG
from ixpeobssim.utils.logging_ import logger


class TestRegionBackscal(unittest.TestCase):

    """Unit test for the BACKSCAL keyword for xpselect with reg files
    """

    def test_region_backscal(self):
        """Compare the reg file BACKSCAL with that of the ordinary circle cut
        of 1'.
        """
        config_file_path = os.path.join(IXPEOBSSIM_CONFIG, 'toy_point_source.py')
        region_file_path = os.path.join(IXPEOBSSIM_TEST_DATA, 'test_reg_backscal.reg')
        logger.info("Generating a toy point source from %s for selection testing...",
                    config_file_path)
        test_file = pipeline.xpobssim(configfile = config_file_path, duration = 1000)
        logger.info("Selecting a circular region from %s...", region_file_path)
        reg_selected = pipeline.xpselect(test_file[0], regfile = region_file_path,
                                         suffix = 'reg', overwrite = True)
        reg_backscal = xEventFile(*reg_selected).backscal()
        logger.info("Selecting a circular region with built-in xpselect function...")
        circ_selected = pipeline.xpselect(test_file[0], rad = 1, suffix = 'circ',
                                          overwrite = True)
        circ_backscal = xEventFile(*circ_selected).backscal()
        assert numpy.allclose(reg_backscal, circ_backscal, rtol = 1e-2)



if __name__ == '__main__':
    unittest.main(exit=not sys.flags.interactive)
