#!/usr/bin/env python
# coding: utf-8

# In[10]:


import openpmd_api as api
import time
import datetime
import numpy as np


# In[11]:


def createCrystal(nc, lc, una, ux, uy, uz):
    x = []
    y = []
    z = []
    for i in range(nc[0]):
        for j in range(nc[1]):
            for k in range(nc[2]):
                for l in range(una):
                    x.append((i + ux[l])*lc[0])
                    y.append((j + uy[l])*lc[1])
                    z.append((k + uz[l])*lc[2])
    return [x,y,z]

# nc is the number of crystal cells and a is the lattice constant
def buildFcc(nc, lc):
    # the number of atoms in an unit cell
    una = 4
    ux = [0.0,0.5,0.5,0.0]
    uy = [0.0,0.5,0.0,0.5]
    uz = [0.0,0.0,0.5,0.5]
    return createCrystal(nc, lc, una, ux, uy, uz)


# In[12]:


# data preparation
# number of cells [nx, ny, nz]
nc = [20, 30, 30]
# lattice constant [a, b, c]
lc = [3.615]*3  # Cu
position_0 = np.asarray(buildFcc(nc,lc))
# number of cells [nx, ny, nz]
nc = [20, 10, 10]
# lattice constant [a, b, c]
lc = [3.615]*3  # Cu
position_1 = np.asarray(buildFcc(nc,lc))


# In[13]:


position_0.shape


# In[14]:


# data flushes into hdf5 file
series = api.Series(
    "dataMD.h5",
    api.Access_Type.create)
# get date
dateNow = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime())

# openPMD standard
series.set_author("Juncheng E <juncheng.e@xfel.eu>")
series.set_openPMD("1.1.0")
series.set_openPMD_extension(0)
series.set_iteration_encoding(api.Iteration_Encoding.group_based)
series.set_particles_path("particles")
series.set_software("LAMMPS")
series.set_software_version("7 Aug 2019")
series.set_date(dateNow)


print("openPMD version: ", series.openPMD)
print("iteration format: ", series.iteration_format)
print("particles path: ", series.particles_path)
print("date: ", series.date)

curStep = series.iterations[0]
curStep.set_time(0.0)        .set_time_unit_SI(1e-15
)
curStep.set_attribute("step",0)
curStep.set_attribute("stepOffset",0)
curStep.set_attribute("timeOffset",0)
curStep.set_attribute("timeUnitSI",1.0)

cu = curStep.particles["Cu"]
d = api.Dataset(position_0[0].dtype, position_0[0].shape)
cu["position"]["x"].reset_dataset(d)
cu["position"]["y"].reset_dataset(d)
cu["position"]["z"].reset_dataset(d)
cu["position"]["x"].set_unit_SI(1.e-10)
cu["position"]["y"].set_unit_SI(1.e-10)
cu["position"]["z"].set_unit_SI(1.e-10)
cu["position"]["x"].store_chunk(position_0[0])
cu["position"]["y"].store_chunk(position_0[1])
cu["position"]["z"].store_chunk(position_0[2])

curStep = series.iterations[22]
cu = curStep.particles["Cu"]
d = api.Dataset(position_1[0].dtype, position_1[0].shape)
cu["position"]["x"].reset_dataset(d)
cu["position"]["y"].reset_dataset(d)
cu["position"]["z"].reset_dataset(d)
cu["position"]["x"].set_unit_SI(1.e-10)
cu["position"]["y"].set_unit_SI(1.e-10)
cu["position"]["z"].set_unit_SI(1.e-10)
cu["position"]["x"].store_chunk(position_1[0])
cu["position"]["y"].store_chunk(position_1[1])
cu["position"]["z"].store_chunk(position_1[2])
series.flush()
del series


# In[15]:


import h5py

f = h5py.File('dataMD.h5', 'r+')
# print ("attributes:")
# for i in f.attrs.items():
#     print ("  ",i)
# print ("groups:")
# for i in f.keys():
#     print ("  ",i)

# get current step
curStep = f['data/0']
for i in curStep.items():
    print (i)

# create ID
cu = curStep['particles/Cu']
ID = cu.create_dataset("id", (position_0.shape[1],1), dtype='i8', data=np.arange(1,position_0.shape[1]+1))

# create group
box = curStep.create_group("box")
observ = curStep.create_group("observables")

# box group
box = curStep["box"]
box.attrs['dimension'] = 3
box.attrs['boundary'] = ['periodic','periodic','periodic']
box.attrs['edge'] = [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]

# observables
observ = curStep["observables"]
temp = observ.create_dataset("temperate", (1,), dtype='f',data=[300])
temp = observ["temperate"]
temp.attrs["unitSI"] = 1.0
vol = observ.create_dataset("volume", (1,), dtype='f', data=[10])
vol.attrs["unitSI"] = 1.0e-30


# In[16]:


f.flush()
f.close()

