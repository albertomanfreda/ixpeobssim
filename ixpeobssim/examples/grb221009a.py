# Copyright (C) 2022, the ixpeobssim team.
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

"""
"""

from __future__ import print_function, division

import numpy

from ixpeobssim.utils.matplotlib_ import plt, setup_gca
import ixpeobssim.core.pipeline as pipeline
import ixpeobssim.config.grb221009a as input_model

def simulate():
    pipeline.xpobssim(duration=input_model.DURATION,
                      startdate=input_model.IXPE_OBS_START,
                      emin=2., emax=8.)

def select():
    pipeline.xpselect(*pipeline.file_list(), emin=2., emax=8.,
                      suffix='selected')

def bin():
    pipeline.xpbin(*pipeline.file_list('selected'), algorithm='LC')
    pipeline.xpbin(*pipeline.file_list('selected'), algorithm='PHA1')
    pipeline.xpbin(*pipeline.file_list('selected'), algorithm='CMAP')

def run():
    simulate()
    select()
    bin()


if __name__ == '__main__':
    pipeline.bootstrap_pipeline('grb221009a')
