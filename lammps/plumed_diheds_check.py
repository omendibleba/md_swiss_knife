#import 
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import argparse

# Write plumed input file to calculate dihedral angles of trajcetory file 


parser = argparse.ArgumentParser(description='REad xyz trajectory and create plumed input to claculate the dihedrals sampled in the trajectory.')
parser.add_argument('xyzfile', help='The name of the xyz trajectory file')

args = parser.parse_args()

with open("plumed_diheds.dat","w") as f:
    print("""
# vim:ft=plumed

# Compute the torsional angle between atoms 1, 10, 20, and 30.
# The angle is called "phi1" for future reference.
phi1: TORSION ATOMS=1,5,8,11 


# Print "phi1" and "phi2" on another file named "COLVAR2" every 100 steps.
PRINT ARG=phi1 FILE=dihedrals_diheds.dat 
#STRIDE=1000 
""",file=f)

# Run the driver with the plumed input file to obtain dihedrals.dat file

subprocess.call(["plumed driver --plumed plumed_diheds.dat --ixyz {}".format(args.xyzfile)],shell=True)
#but1_t7_nvt_clmd.xyz

# Read dihedrals.dat file 

dihedrals = np.loadtxt("dihedrals_diheds.dat",skiprows=1)

# Make a figure that includes the two plots from above in two columns 

fig, (ax1, ax2) = plt.subplots(1, 2,figsize=(12,5))
# Add title to figure 
fig.suptitle('Sampled Dihedral Angles in Training Data',fontsize=16,fontweight='bold')
ax1.plot(dihedrals[:,1],'x')
ax1.set_xlabel("Frame", fontsize=14)
ax1.set_ylabel("Dihedral angle (rad)", fontsize=14)
#ax1.set_xticks(fontsize=11)
ax2.hist(dihedrals[:,1],bins=100)
ax2.set_xticks(np.arange(-np.pi,np.pi+np.pi/4,np.pi/4),["-180","-135","-90","-45","0","45","90","135","180"])
#ax2.set_title('Sampled DIhedrals  in training data',fontsize=16,fontweight='bold')
ax2.set_xlabel("Dihedral angle (degrees)",fontsize=14)
ax2.set_ylabel("Frequency",fontsize=14)
#ax2.set_xticks(fontsize=11)
plt.savefig("diheds.png",dpi=300)
plt.show()

