#!/usr/bin/env python
# coding: utf-8

# In[1]:


import openpmd_api as api
import time
import datetime
import numpy as np
from numpy.random import random
SCALAR = api.Mesh_Record_Component.SCALAR
Unit_Dimension = api.Unit_Dimension


# In[2]:


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


# In[3]:


# data preparation
# number of cells [nx, ny, nz]
nc = [3, 3, 3]
# lattice constant [a, b, c]
lc = [3.615]*3  # Cu
position_0 = np.asarray(buildFcc(nc,lc))
position_1 = position_0 + random(position_0.shape)*5
velocity_0 = random(position_0.shape)*1000
velocity_1 = random(position_1.shape)*1000
id = np.arange(1,position_0.shape[1]+1)


# In[4]:


print (position_0.shape)
print (id.shape)


# In[5]:


# data flushes into hdf5 file
series = api.Series(
    "dataMD_extended.h5",
    api.Access_Type.create)
# get date
dateNow = time.strftime('%Y-%m-%d %H:%M:%S %z', time.localtime())


# In[6]:


# default series settings
print("Default settings:")
print("basePath: ", series.base_path)
print("openPMD version: ", series.openPMD)
print("iteration format: ", series.iteration_format)


# In[7]:


# openPMD standard
series.set_openPMD("1.1.0")
series.set_openPMD_extension(0)
series.set_author("Juncheng E <juncheng.e@xfel.eu>")
series.set_particles_path("particles")
series.set_date(dateNow)
series.set_iteration_encoding(api.Iteration_Encoding.group_based)
series.set_software("LAMMPS")
series.set_software_version("7 Aug 2019")
series.set_attribute("forceField",["lj/cut 3.0","eam/alloy"])
series.set_attribute("forceFieldParameter",["pair_coeff * * 1 1","pair_coeff 1 1 Cu_mishin1.eam.alloy Cu"])

curStep = series.iterations[0]
curStep.set_time(0.0)        .set_time_unit_SI(1e-15)
curStep.set_attribute("step",np.uint64(0))
curStep.set_attribute("stepOffset",np.uint64(0))
curStep.set_attribute("timeOffset",np.float32(0))

cu = curStep.particles["Cu"]

# id data
d = api.Dataset(id.dtype, id.shape)
cu["id"][SCALAR].reset_dataset(d)
cu["id"][SCALAR].store_chunk(id)


# In[8]:


# position data
d = api.Dataset(position_0[0].dtype, position_0[0].shape)
cu["position"]["x"].reset_dataset(d)
cu["position"]["y"].reset_dataset(d)
cu["position"]["z"].reset_dataset(d)
cu["position"]["x"].set_unit_SI(1.e-10)
cu["position"]["y"].set_unit_SI(1.e-10)
cu["position"]["z"].set_unit_SI(1.e-10)
cu["position"].set_unit_dimension({Unit_Dimension.L: 1})
cu["position"]["x"].store_chunk(position_0[0])
cu["position"]["y"].store_chunk(position_0[1])
cu["position"]["z"].store_chunk(position_0[2])
# velocity data
d = api.Dataset(velocity_0[0].dtype, velocity_0[0].shape)
cu["velocity"]["x"].reset_dataset(d)
cu["velocity"]["y"].reset_dataset(d)
cu["velocity"]["z"].reset_dataset(d)
cu["velocity"]["x"].set_unit_SI(1.e-10)
cu["velocity"]["y"].set_unit_SI(1.e-10)
cu["velocity"]["z"].set_unit_SI(1.e-10)
cu["velocity"].set_unit_dimension({Unit_Dimension.L: 1, Unit_Dimension.T: -1})
cu["velocity"]["x"].store_chunk(velocity_0[0])
cu["velocity"]["y"].store_chunk(velocity_0[1])
cu["velocity"]["z"].store_chunk(velocity_0[2])

curStep = series.iterations[1]
cu = curStep.particles["Cu"]
d = api.Dataset(id.dtype, id.shape)
cu["id"][SCALAR].reset_dataset(d)
cu["id"][SCALAR].store_chunk(id)

d = api.Dataset(position_1[0].dtype, position_1[0].shape)
cu["position"]["x"].reset_dataset(d)
cu["position"]["y"].reset_dataset(d)
cu["position"]["z"].reset_dataset(d)

cu["position"].set_unit_dimension({Unit_Dimension.L: 1})
cu["position"]["x"].set_unit_SI(1.e-10)
cu["position"]["y"].set_unit_SI(1.e-10)
cu["position"]["z"].set_unit_SI(1.e-10)

cu["position"]["x"].store_chunk(position_1[0])
cu["position"]["y"].store_chunk(position_1[1])
cu["position"]["z"].store_chunk(position_1[2])

d = api.Dataset(velocity_1[0].dtype, velocity_1[0].shape)
cu["velocity"]["x"].reset_dataset(d)
cu["velocity"]["y"].reset_dataset(d)
cu["velocity"]["z"].reset_dataset(d)

cu["velocity"].set_unit_dimension({Unit_Dimension.L: 1, Unit_Dimension.T: -1})
cu["velocity"]["x"].set_unit_SI(1.e-10)
cu["velocity"]["y"].set_unit_SI(1.e-10)
cu["velocity"]["z"].set_unit_SI(1.e-10)

cu["velocity"]["x"].store_chunk(velocity_1[0])
cu["velocity"]["y"].store_chunk(velocity_1[1])
cu["velocity"]["z"].store_chunk(velocity_1[2])


# In[9]:


series.flush()
del series


# In[10]:


import h5py

f = h5py.File('dataMD_extended.h5', 'r+')
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

# create group
box = curStep.create_group("box")
observ = curStep.create_group("observables")

# box group
box = curStep["box"]
box.attrs['dimension'] = np.uint64(3)
box.attrs['boundary'] = ['periodic','periodic','periodic']
box.attrs['edge'] = [[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]]

# observables
observ = curStep["observables"]
temp = observ.create_dataset("temperate", (1,), dtype='f',data=[300])
temp = observ["temperate"]
temp.attrs["unitSI"] = 1.0
vol = observ.create_dataset("volume", (1,), dtype='f', data=[10])
vol.attrs["unitSI"] = 1.0e-30


# In[11]:


f.flush()
f.close()

