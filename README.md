# Domain-Specific Naming Conventions for Molecular Dynamics Simulation Codes

## Data structure notations

`/-- item` *Either a dataset or a group, indented by one space to its parent group. If it is a group itself, the objects within the group are indented by five spaces with respect to the group name.*

`+-- attribute` *An attribute, that relates either to a group or a dataset.*

`/-- dataset: <type>[dim1][dim2] {value}` *A dataset with a `[dim1 x dim2]` array and of type `<type>`. The value of the data is `{value}`.*

## Data structure example
Example file: [](./dataMD.h5)

```
Root
 +-- openPMD: <string>[] {1.1.0}
 +-- openPMDextension: <unit64>[1] {2}
 +-- author: <string>[] {Juncheng E <juncheng.e@xfel.eu>} 
 +-- basePath: <string>[] {/data/}
 +-- particlePath: <string>[] {particles/}
 +-- date: <string>[] {2019-09-05 20:45:02 +0200}
 +-- iterationEncoding: <string>[] {groupBased}
 +-- interationFormat: <string>[] {/data/%T}
 +-- software: <string>[] {LAMMPS}
 +-- softwareVersion: <string>[] {7 Aug 2019}
      /-- data
           /-- 0
            +-- dt: <float64>[1] {1.0}
            +-- step: <unit64>[1] {0}
            +-- stepOffset: <unit64>[1] {0}
            +-- time: <float64>[1] {0.0}
            +-- timeOffset: <float64>[1] {0.0}
            +-- timeUnitSI: <float64>[1] {1.0e-12}
                /-- box
                 +-- boundary: <string>[3] {[periodic,periodic,periodic]}
                 +-- dimension: <unit64>[1] {3}
                 +-- edge: <float64>[3][3] {[[1,0,0],[0,1,0],[0,0,1]]}
                 +-- limit: <float64>[3][2] {[[0,300],[0,300],[0,300]]}
                 +-- unitSI: <float64>[1] {1.0e-10}
                /-- observables
                 /-- temprerature: <float64>[1] {300}
                  +-- unitSI: <float64>[1] {1.0} 
                 /-- volume: <float64>[1] {27}
                  +-- unitSI: <float64>[1] {1.0e-24}
                /--  particles
                     /-- Cu
                      /-- id: <uint64>[72000]
                          /-- position
                           +-- timeOffset: <float64>[1] {0.0}
                           +-- unitDimension: <float64>[7] {[1,0,0,0,0,0,0]}
                               /-- x: <float64>[72000]
                                +-- unitSI: <float64>[1.0e-10]
                               /-- y: <float64>[72000]
                                +-- unitSI: <float64>[1.0e-10]
                               /-- z: <float64>[72000]
                                +-- unitSI: <float64>[1.0e-10]
```
## References
* LAMMPS h5md dump 
https://lammps.sandia.gov/doc/dump_h5md.html
* LAMMPS triclinic simulation box
https://lammps.sandia.gov/doc/Howto_triclinic.html
* h5md webpage
https://nongnu.org/h5md/
* h5md paper
[de Buyl, Colberg and Hofling, H5MD: A structured, efficient, and portable file format for molecular data, Comp. Phys. Comm. 185(6), 1546-1553 (2014)](https://www.sciencedirect.com/science/article/pii/S0010465514000447)
* Atomeye cfg standard 
http://li.mit.edu/Archive/Graphics/A/#extended_CFG

