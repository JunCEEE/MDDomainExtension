##########################################################################
#                                                                        #
# Copyright (C) 2019 Juncheng E                                          #
# Contact: juncheng E <juncheng.e@xfel.eu>                               #
#                                                                        #
# This file is part of SimEx python library.                             #
# SimEx is free software: you can redistribute it and/or modify          #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                        #
# SimEx is distributed in the hope that it will be useful,               #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                        #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#                                                                        #
##########################################################################

# initialize
import os
from argparse import ArgumentParser
import numpy as np
import h5py
import openpmd_api as api
from mendeleev import element
import warnings

warnings.simplefilter("ignore")

def convertToOPMD(input_path):
    # output setting
    output_path = os.path.splitext(input_path)[0]+'.opmd'+'.h5'
    if os.path.isfile(output_path):
        overwrite = input(output_path+" existed, overwrite? [y/n]").strip()
        if (overwrite == "y"): 
            os.remove(output_path)
            print (output_path+" overwritten")
        else:
            print ('did not overwrite, exit.')
            exit()

    # record running time
    import atexit
    from time import time, strftime, localtime
    from datetime import timedelta

    def secondsToStr(elapsed=None):
        if elapsed is None:
            return strftime("%Y-%m-%d %H:%M:%S", localtime())
        else:
            return str(timedelta(seconds=elapsed))

    def log(s, elapsed=None):
        line = "="*40
        print(line)
        print(secondsToStr(), '-', s)
        if elapsed:
            print("Elapsed time:", elapsed)
        print(line)

    def endlog():
        end = time()
        elapsed = end-start
        log("End Program", secondsToStr(elapsed))

    start = time()
    atexit.register(endlog)
    log("Start Program")

    # set output hierarchy
    series = api.Series(
        output_path,
        api.Access_Type.create)
    series.set_openPMD("1.1.0")
    series.set_openPMD_extension(2)
    series.set_iteration_encoding(api.Iteration_Encoding.group_based)
    series.set_software("XMDYN")

    # convert from XMDYN to openPMD
    xmdyn_attributes = dict()
    with h5py.File(input_path, 'r') as xmdyn_h5:

        # from misc
        xmdyn_path = 'misc/run/start_0'
        try:
            xmdyn_attributes['date'] = xmdyn_h5[xmdyn_path][()]
            series.set_software_version(xmdyn_attributes['date'])
        except KeyError:
            warnings.warn(xmdyn_path+' does not exist in xmdyn_h5', Warning)

        # from params
        xmdyn_path = 'params/xparams'
        try:
            xmdyn_attributes['comment'] = xmdyn_h5[xmdyn_path][()].decode('ascii')
            series.set_comment(xmdyn_attributes['comment'])
        except KeyError:
            warnings.warn(xmdyn_path+' does not exist in xmdyn_h5', Warning)

        # from info
        xmdyn_path = 'info/package_version'
        try:
            xmdyn_attributes['version'] = xmdyn_h5[xmdyn_path][()]
            series.set_software_version(xmdyn_attributes['version'])
        except KeyError:
            warnings.warn(xmdyn_path+' does not exist in xmdyn_h5', Warning)
            
        xmdyn_path = 'info/package_version'
        try: 
            xmdyn_attributes['forceField'] = xmdyn_h5[xmdyn_path][()].decode('ascii')
            series.set_attribute('forceField', xmdyn_attributes['forceField'])
        except KeyError:
            warnings.warn(xmdyn_path+' does not exist in xmdyn_h5', Warning)

        t0 = 0
        for it in range(1, 3):
            # it += 1
            snp = 'snp_'+str(it).zfill(7)
            curStep = series.iterations[it]

            try:
                # set real time for each step
                t1 = xmdyn_h5['misc/time/'+snp][0]
                dt = t1-t0
                curStep.set_time(t1) .set_time_unit_SI(1) .set_dt(dt)
                # for next loop
                t0 = t1
            except KeyError:
                warnings.warn(
                    'misc/time/'+' does not exist in xmdyn_h5', Warning)

            # convert position
            Z = xmdyn_h5['data/'+snp]['Z']
            r = xmdyn_h5['data/'+snp]['r']
            uZ = np.sort(np.unique(Z))

            for z in uZ:
                # get element symbol
                particle = curStep.particles[element(int(z)).symbol]
                particle["position"].set_attribute(
                    "coordinate", "absolute")
                particle["position"].set_unit_dimension(
                    {api.Unit_Dimension.L: 1})
                position = r[Z[:] == z, :]
                p_list = []
                for ax in range(3):
                    p_list.append(position[:, ax].astype(np.float64))
                dShape = api.Dataset(p_list[0].dtype, p_list[0].shape)
                particle["position"]["x"].reset_dataset(dShape)
                particle["position"]["y"].reset_dataset(dShape)
                particle["position"]["z"].reset_dataset(dShape)
                for i, axis in enumerate(particle["position"]):
                    particle["position"][axis].set_unit_SI(1.0)
                    particle["position"][axis].store_chunk(p_list[i])
                series.flush()
            print(it)

        print('number of snapshots:', it)
    del series

if __name__ == "__main__":

    # Parse arguments.
    parser = ArgumentParser(description="Convert XMDYN output to openPMD-conforming hdf5. [v0.1]")
    parser.add_argument("input_file", metavar="input_file",
                      help="name of the file to convert.")
    args = parser.parse_args()

    # Call the converter routine.
    convertToOPMD(args.input_file)