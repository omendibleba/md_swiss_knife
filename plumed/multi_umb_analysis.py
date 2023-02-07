import plumed
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wham
import subprocess
import concurrent.futures
import os

# Define variables 
n_umbs = 32
n_frames = 2001
T=300
kB=8.314462618*0.001


# Create a python code that concatenates the trajectories from each umbrella simulation 
# specify the base directory where the umbrella_i folders are located
base_dir = '.'

# open the output file for writing
with open('tot_umbs_traj.xyz', 'w') as outfile:
    for i in range(n_umbs):
        # construct the path to the current folder
        folder_path = os.path.join(base_dir, 'umbrella_{}'.format(i))
        
        # check if the current folder exists
        if os.path.exists(folder_path):
            # construct the path to the xyz file in the current folder
            xyz_file = os.path.join(folder_path, 'but1_test.xyz')
            
            # check if the xyz file exists in the current folder
            if os.path.exists(xyz_file):
                # open the xyz file for reading
                with open(xyz_file, 'r') as infile:
                    # read the contents of the xyz file
                    contents = infile.read()
                    
                    # write the contents of the xyz file to the output file
                    outfile.write(contents)
            else:
                print(f"The file {xyz_file} was not found in folder {folder_path}")
        else:
            print(f"The folder {folder_path} was not found.")

print("The concatenation process has finished.")


# ## RUn the driver to get the energies related to the biasing potential 
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
    for i in range(n_umbs):

        #print("Running umbrella_{}".format(i))
        executor.submit(subprocess.run,"plumed driver --plumed umbrella_{}/plumed_{}.dat --ixyz tot_umbs_traj.xyz --trajectory-stride 1000".format(i,i),shell=True)



# Plot hte phi angles sampled as a function of the added simulatino time
col=[]
for i in range(n_umbs):
    col.append(plumed.read_as_pandas("colvar_multi_" + str(i)+".dat"))
# notice that this is the concatenation of 32 trajectories with 2001 frames each
    plt.plot(col[i].time[n_frames*i:n_frames*(i+1)],col[i].phi[n_frames*i:n_frames*(i+1)],"x")
plt.xlabel("Sampled $\phi$",fontsize=14)
plt.ylabel("Added Trajectory Frames",fontsize=14)
plt.savefig('multi_umbrella_CVs_sampled.png')
plt.show()


# Calculate and plot the log Weight of each bias calculated with the WHAM analysis 
bias=np.zeros((len(col[0]["bb.bias"]),32))
for i in range(32):
    bias[:,i]=col[i]["bb.bias"][-len(bias):]
w=wham.wham(bias,T=kB*T)
plt.plot(w["logW"])
plt.xlabel("Added Biased Simulation Trajectories",fontsize=14)
plt.ylabel("Log Weight",fontsize=14)
plt.savefig('multi_umbrella_logW.png')
plt.show()


# add the log weight to the colvar file
colvar = col[0]
colvar["logweights"]=w["logW"]

# Save the colvar file with the log weights
plumed.write_pandas(colvar,"bias_multi.dat")


# Create the plumed_multi.dat file to compute the free energy surface
with open("plumed_multi.dat","w") as f:
    print("""
# vim:ft=plumed
phi: READ FILE=bias_multi.dat VALUES=phi IGNORE_TIME
lw: READ FILE=bias_multi.dat VALUES=logweights IGNORE_TIME

# use the command below to compute the histogram of phi
# we use a smooth kernel to produce a nicer graph here
hhphi: HISTOGRAM ARG=phi GRID_MIN=-pi GRID_MAX=pi GRID_BIN=600 BANDWIDTH=0.05
ffphi: CONVERT_TO_FES GRID=hhphi TEMP=300 # no need to set TEMP here, PLUMED will obtain it from GROMACS
DUMPGRID GRID=ffphi FILE=fes_phi_cat.dat


# we use a smooth kernel to produce a nicer graph here
hhphir: HISTOGRAM ARG=phi GRID_MIN=-pi GRID_MAX=pi GRID_BIN=600 BANDWIDTH=0.05 LOGWEIGHTS=lw
ffphir: CONVERT_TO_FES GRID=hhphir TEMP=300 # no need to set TEMP here, PLUMED will obtain it from GROMACS
DUMPGRID GRID=ffphir FILE=fes_phi_catr.dat

""",file=f)


# Run the driver to compute the free energy surface
subprocess.run("plumed driver --noatoms --plumed plumed_multi.dat --kt {}".format(kB*T),shell=True)


## Read the files of the calculated free energy 
fes_phi_bias = plumed.read_as_pandas("fes_phi_cat.dat").replace([np.inf, -np.inf], np.nan).dropna()
fes_phi_bias_recover=plumed.read_as_pandas("fes_phi_catr.dat").replace([np.inf, -np.inf], np.nan).dropna()

## Plot the biased and recover free energies 
plt.plot(fes_phi_bias.phi,fes_phi_bias.ffphi,label="biased")

plt.plot(fes_phi_bias_recover.phi,fes_phi_bias_recover.ffphir,label="reweighted")
plt.legend()
plt.xlim((-np.pi,np.pi))
plt.xlabel("$\phi$" ,fontsize=14)
plt.ylabel("$F(\phi)$ (kj/mol",fontsize=14)
plt.savefig('multi_umbrella_fes.png')
plt.show()