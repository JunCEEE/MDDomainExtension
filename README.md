# Domain-Specific Naming Conventions for Molecular Dynamics Simulation Codes - Data Structure

## Data structure notations

`/-- item` *Either a dataset or a group, indented by 4 spaces to its parent group.*

`+-- attribute` *An attribute, indented by 1 space to its relateed group or dataset.*

`/-- dataset: <type>[dim1][dim2] {value}` *A dataset with a `[dim1 x dim2]` array and of type `<type>`. The value of the data is `{value}`.*

## Data structure example 
This example is conforming to [openPMD MD extension](https://github.com/ejcjason/openPMD-standard/blob/EXT_MD/EXT_MD.md) (draft), and can be written with [openPMD-api](https://github.com/openPMD/openPMD-api) directly without observables.
```
Root
 +-- openPMD: <string>[] {1.1.0}
 +-- openPMDextension: <unit64>[1] {2}
 +-- author: <string>[] {Juncheng E <juncheng.e@xfel.eu>} 
 +-- basePath: <string>[] {/data/%T/}
 +-- particlesPath: <string>[] {particles/}
 +-- date: <string>[] {2019-09-05 20:45:02 +0200}
 +-- iterationEncoding: <string>[] {groupBased}
 +-- interationFormat: <string>[] {/data/%T}
 +-- software: <string>[] {LAMMPS}
 +-- softwareVersion: <string>[] {7 Aug 2019}
 +-- forceField: <string>[] {["lj/cut 3.0","eam/alloy"]}
 +-- forceFieldParameter: <string>[] {["pair_coeff * * 1 1","pair_coeff 1 1 Cu_mishin1.eam.alloy Cu"]}
 +-- comment: <string>[] {"NPT, temperature was reduced by 100 K every 5000 steps."}
    /-- data
        /-- 0
         +-- dt: <float64>[1] {1.0}
         +-- time: <float32>[1] {0.0}
         +-- timeUnitSI: <float64>[1] {1.0e-12}
            /-- observables <optional, openPMD API incompatible>
                /-- temprerature: <float64>[1] {300}
                 +-- unitSI: <float64>[1] {1.0} 
                /-- volume: <float64>[1] {27}
                 +-- unitSI: <float64>[1] {1.0e-24}
                /-- pressure: <float64>[1] {200}
                 +-- unitSI: <float64>[1] {1e6}
            /-- particles
                /-- Cu
                    /-- id: <uint64>[108]
                    /-- box <optional>
                     +-- boundary: <string>[3] {["periodic","periodic","periodic"]}
                     +-- dimension: <unit32>[1] {3}
                        /-- edge: <float64>[3][3] {[[1,0,0],[0,1,0],[0,0,1]]}
                        /-- limit: <float64>[3][2] {[[0,300],[0,300],[0,300]]}
                         +-- unitSI: <float64>[1] {1.0e-10}
                    /-- position
                     +-- timeOffset: <float64>[1] {0.0}
                     +-- unitDimension: <float64>[7] {[1,0,0,0,0,0,0]}
                     +-- coordinate: <string>[] {absolute}
                        /-- x: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- y: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- z: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                    /-- velocity
                     +-- timeOffset: <float64>[1] {0.0}
                     +-- unitDimension: <float64>[7] {[1,0,0,0,0,0,0]}
                        /-- x: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- y: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- z: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                /-- C
                    /-- id: <uint64>[108]
                    /-- box
                     +-- boundary: <string>[3] {["periodic","periodic","periodic"]}
                     +-- dimension: <unit32>[1] {3}
                        /-- edge: <float64>[3][3] {[[1,0,0],[0,1,0],[0,0,1]]}
                        /-- limit: <float64>[3][2] {[[0,300],[0,300],[0,300]]}
                         +-- unitSI: <float64>[1] {1.0e-10}
                    /-- position
                     +-- timeOffset: <float64>[1] {0.0}
                     +-- unitDimension: <float64>[7] {[1,0,0,0,0,0,0]}
                     +-- coordinate: <string>[] {absolute}
                        /-- x: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- y: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- z: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                    /-- velocity
                     +-- timeOffset: <float64>[1] {0.0}
                     +-- unitDimension: <float64>[7] {[1,0,0,0,0,0,0]}
                        /-- x: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- y: <float64>[108]
                         +-- unitSI: <float64>[1.0e-10]
                        /-- z: <float64>[108]
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
* Interatomic potentials (Force Fields)
https://www.ctcms.nist.gov/potentials/
https://en.wikipedia.org/wiki/Force_field_(chemistry)
https://www.sciencedirect.com/science/article/pii/S1359028613000788

