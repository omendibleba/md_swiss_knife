# Import libraries 

import plumed
import matplotlib.pyplot as plt
import numpy as np
import pandas
# import wham
import subprocess
import concurrent.futures
import os 


# Number of umbrellas 
n_umbs = 32

# This are the centers for each umbrella 
at=np.linspace(-np.pi,np.pi,n_umbs+1)[:-1]


## Define inputs for plumed
for i in range(n_umbs):

    with open("plumed_"+str(i)+".dat","w") as f:
        print("""

# phi: TORSION ATOMS=1,5,8,11
phi: TORSION ATOMS=1,2,3,4
bb: RESTRAINT ARG=phi KAPPA=100.0 AT={}

lw: REWEIGHT_BIAS TEMP=600

hhphi: HISTOGRAM ARG=phi STRIDE=1000 GRID_MIN=-pi GRID_MAX=pi GRID_BIN=600 BANDWIDTH=0.05

ffphi: CONVERT_TO_FES GRID=hhphi TEMP=600

DUMPGRID GRID=ffphi FILE=fes_phi_biased1.dat STRIDE=500000

# we use a smooth kernel to produce a nicer graph here
hhphir: HISTOGRAM ARG=phi STRIDE=1000 GRID_MIN=-pi GRID_MAX=pi GRID_BIN=600 BANDWIDTH=0.05 LOGWEIGHTS=lw
ffphir: CONVERT_TO_FES GRID=hhphir TEMP=600  # no need to set TEMP here, PLUMED will obtain it from GROMACS
DUMPGRID GRID=ffphir FILE=fes_phi_biased1r.dat STRIDE=500000 # stride is needed here since PLUMED does not know when the simulation is ov


PRINT ARG=phi,bb.bias,lw STRIDE=100 FILE=colvar_multi_{}.dat """.format(at[i],i),file=f)



## Define inputs for lammps that specify the input for plummed
for i in range(n_umbs):

    with open("but1_umbrella_"+str(i)+".inp","w") as f:
        print("""
units	real
atom_style atomic
newton off
thermo 1
read_data but1.data

pair_style	nequip
pair_coeff	* * mod_but1_rc10.pth C H
mass            1 12.011  ##15.9994
mass            2 1.00794

neighbor 1.0 bin
neigh_modify delay 5 every 1

timestep        1
thermo 1000

thermo_style    custom step time etotal ke pe temp press vol

velocity all create 600 54323
fix 1 all nvt temp 600 600 100

fix pl all plumed plumedfile plumed_{}.dat outfile plumed.log

dump myDump all custom 1000 forces.dump id type x y z fx fy fz
dump mydumpxyz all xyz 1000 traj_nnip.xyz

run 500000 """.format(i),file=f)


# Define submission files 
## Define inputs for plumed
for i in range(n_umbs):

    with open("sub_umb_"+str(i)+".sh","w") as f:
        print("""#!/bin/bash

#$ -pe smp 1     # Specify parallel environment and legal core size
#$ -q hpc@@colon           # Specify queue
#$ -N NaCl_umb_multi      # Specify job name

#module load lammps      # Required modules

module load cuda/11.0 cudnn/8.0.4 cmake/3.19.2 gsl/gcc/2.7 pytorch/1.13 mpich/3.3/gcc/8.5.0

lmp_nequip_plumed -in but1_umbrella_{}.inp

""".format(i),file=f)



# This is the script to generate the folders and move the plumed files inside them
with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    for i in range(n_umbs):
        folder_name = "umbrella_" + str(i)
        os.mkdir(folder_name)
        file_name = "plumed_" + str(i) + ".dat"
        os.rename(file_name, folder_name + "/" + file_name)

        # Move input file into repective umbrella directory 
        #executor.submit(subprocess.run,"mv but1_umbrella_{}.inp umbrella_{}".format(i,i),shell=True)
        executor.submit(subprocess.run,["mv", "but1_umbrella_{}.inp".format(i), "umbrella_{}".format(i)])

        # Copy  input file and data file into
        executor.submit(subprocess.run,"cp but1.data mod_but1_rc10.pth umbrella_{}".format(i),shell=True)

        # COpy submission file to each folde 
        executor.submit(subprocess.run,"mv sub_umb_{}.sh umbrella_{}".format(i,i),shell=True)

    