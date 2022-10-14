#!/urs/bin/env python
#
# Copyright (C) 2015--2020, the ixpeobssim team.
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

"""Spectral facilities.
"""

from __future__ import print_function, division

import sys

import numpy

from ixpeobssim.core.rand import xUnivariateGenerator, xUnivariateAuxGenerator
from ixpeobssim.core.spline import xUnivariateSpline
from ixpeobssim.utils.units_ import erg_to_keV
from ixpeobssim.utils.logging_ import logger
from ixpeobssim.utils.fmtaxis import fmtaxis

# pylint: disable=invalid-name, too-many-arguments



def load_light_curve_data(file_path, time_column=0, flux_column=1,
                          time_offset=0., erg=False, delimiter=None, **kwargs):
    """Routine to parse light curve tabular data from ASCII files.

    You can use this whenever you have a data file where one of the
    columns (typically the first) indicates the time, and one of the
    others contain the flux.

    Args
    ----
    file_path : str
        The path to the ASCII file containing the data.

    time_column : int, default to 0
        The identifier of the column containing the time values (in seconds).

    flux_column : int, default to 1
        The identifier of the column containing the flux values

    time_offset : float, default to 0.
        The offset (in MET) compared to which the times are expressed

    erg : bool, default to False
        Wheter the flux is in erg/cm^2/s (if False we assume kev/cm^2/s)
    """
    logger.info('Loading tabular data from %s...', file_path)
    data = numpy.loadtxt(file_path, delimiter=delimiter, unpack=True)
    time = data[time_column] + time_offset
    flux = data[flux_column]
    if erg:
        flux = erg_to_keV(flux)
    logger.info('Done, %d columns and %d rows read out.', len(data), time.size)
    kwargs.update(fmtaxis.light_curve)
    return xUnivariateSpline(time, flux, **kwargs)
