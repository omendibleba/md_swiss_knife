#! /usr/bin/env python3
""""
THis script read the output of the lammps driver which contains the time and distance between two atoms 

"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile

parser = argparse.ArgumentParser(description='Plot the temperature from a LAMMPS log file')
parser.add_argument('plumed_output_file', help='The name of the PLummed output file. Contains distance betwewen two atoms')

args = parser.parse_args()

#read the output file from plumed driver 
data = np.loadtxt(args.plumed_output_file)

# Read the time and distance
time = data[:,0]
dist = data[:,1]

# PLot a histogram of the distance

plt.hist(dist, bins=50)
plt.xlabel('Distance (Angstrom)', fontsize=14,fontweight='bold')
plt.ylabel('Frequency', fontsize=14,fontweight='bold')
plt.title('Histogram of the distance between Na and Cl', fontsize=18,fontweight='bold')
plt.savefig('histogram_COM.png')
plt.show()
