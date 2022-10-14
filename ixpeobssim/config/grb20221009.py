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
import os

from ixpeobssim import IXPEOBSSIM_CONFIG_ASCII, IXPEOBSSIM_SRCMODEL
from ixpeobssim.utils.matplotlib_ import plt, setup_gca
from ixpeobssim.srcmodel.roi import xROIModel, xExtendedSource
from ixpeobssim.srcmodel.spectrum import power_law
from ixpeobssim.srcmodel.polarization import constant
from ixpeobssim.srcmodel.light_curve import load_light_curve_data
from ixpeobssim.utils.time_ import string_to_met_utc
from ixpeobssim.config import file_path_to_model_name
from ixpeobssim.srcmodel.bkg import xPowerLawInstrumentalBkg
from ixpeobssim.utils.logging_ import logger

__model__ = file_path_to_model_name(__file__)

PL_INDEX = 1.71
POL_DEG = 0.2
POL_ANG = 40.
N_H = 5.36e21
SWIFT_FLUX_EMIN = 0.3
SWIFT_FLUX_EMAX = 10.
SRC_RA, SRC_DEC = 288.26452, 19.77350
SRC_REDSHIFT = 0.151
SWIFT_OBS_START = "2022-10-09T14:10:17.000"
SWIFT_OBS_MET = string_to_met_utc(SWIFT_OBS_START)
IXPE_OBS_START = "2022-10-11T23:14:00.000"
IXPE_OBS_MET = string_to_met_utc(IXPE_OBS_START)
DURATION = 100000

swift_light_curve = load_light_curve_data(os.path.join(IXPEOBSSIM_CONFIG_ASCII,
                                          'grb221009A_lightcurve.csv'),
                                          flux_column=3, erg=True, k=3,
                                          s=100, time_offset=SWIFT_OBS_MET)

SWIFT_IMAGE_PATH = (os.path.join(IXPEOBSSIM_SRCMODEL, 'fits',
                   'grb221009a_swift_xrt_1p5_10_keV_image.fits'))

def pl_norm():
    """ Conversion factor between the flux and the normalization of the power
    law. Note that this is the unabsorbed flux."""
    idx = 2 - PL_INDEX
    conversion_factor = idx / (SWIFT_FLUX_EMAX**idx - SWIFT_FLUX_EMIN**idx)
    logger.info(f'Conversion factor from flux to PL norm = {conversion_factor}')
    def _pl_norm(t):
        return conversion_factor * swift_light_curve(t)
    return _pl_norm


spec = power_law(pl_norm(), PL_INDEX)
pol_deg = constant(POL_DEG)
pol_ang = constant(numpy.radians(POL_ANG))

src = xExtendedSource(name='GRB221009A',
                      img_file_path=SWIFT_IMAGE_PATH,
                      photon_spectrum=spec,
                      polarization_degree=pol_deg,
                      polarization_angle=pol_ang,
                      column_density=N_H,
                      redshift=SRC_REDSHIFT)
ROI_MODEL = xROIModel(SRC_RA, SRC_DEC, src)
#Add also the instrumental background
bkg = xPowerLawInstrumentalBkg()
ROI_MODEL.add_source(bkg)

def display():
    """Display he original light curve and image, as well as the power law
    normalization as a function of time.
    """
    plt.figure(f'light curve {__model__}')
    swift_light_curve.plot(logx=True, logy=True, label='SWIFT LC')
    plt.fill_betweenx(swift_light_curve.y, IXPE_OBS_MET, IXPE_OBS_MET + DURATION,
                      color='lightblue', alpha=0.4, label='IXPE obs')
    plt.xlim((swift_light_curve.xmin(), swift_light_curve.xmax()))
    top_xaxis = plt.gca().secondary_xaxis('top',
            functions=(lambda x: x-SWIFT_OBS_MET, lambda x: x+SWIFT_OBS_MET))
    top_xaxis.set_xlabel('Time since SWIFT trigger [s]')
    plt.legend()
    plt.tight_layout()

    plt.figure(f'PL norm {__model__}')
    t_ = numpy.linspace(IXPE_OBS_MET, IXPE_OBS_MET + DURATION, 200)
    plt.plot(t_, pl_norm()(t_), 'o')
    setup_gca(xlabel='MET[s]', ylabel='PL. Norm [cm-2 s-1 keV-1]')
    top_xaxis_2 = plt.gca().secondary_xaxis('top',
            functions=(lambda x: x-SWIFT_OBS_MET, lambda x: x+SWIFT_OBS_MET))
    top_xaxis_2.set_xlabel('Time since SWIFT trigger [s]')
    plt.tight_layout()


if __name__ == '__main__':
    from ixpeobssim.config import bootstrap_display
    bootstrap_display()
