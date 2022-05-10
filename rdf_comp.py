import numpy as np 
import os
import matplotlib.pyplot as plt

#Create file to store outputs 
path = os.getcwd()
try:
    os.mkdir(path+"/rdf_comp")
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)


# Load rdf files from VMD. CHange the name or ad as needed.

model_name = ' (Model 5K x05) \n'

#From CP2K``
rdf_cp2k_2kmod_HO = np.loadtxt('../rdf_cp2k_5kmod_H-O.dat')
rdf_cp2k_2kmod_HH = np.loadtxt('../rdf_cp2k_5kmod_H-H.dat')
rdf_cp2k_2kmod_OO = np.loadtxt('../rdf_cp2k_5kmod_O-O.dat')

#From Lammps
rdf_lmp_2kmod_HO = np.loadtxt('rdf_lmp_5kmodx05_H-O.dat')
rdf_lmp_2kmod_HH = np.loadtxt('rdf_lmp_5kmodx05_H-H.dat')
rdf_lmp_2kmod_OO = np.loadtxt('rdf_lmp_5kmodx05_O-O.dat')


# Read H-O gr data from both simulations 

# AIMD
r_HO = rdf_cp2k_2kmod_HO[:,0]
gr_HO = rdf_cp2k_2kmod_HO[:,1]

# Lammps
r_lmp_HO = rdf_lmp_2kmod_HO[:,0]
gr_lmp_HO = rdf_lmp_2kmod_HO[:,1]


#PLot and compare rdf from AIMD and Lammps 
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(r_HO,gr_HO,color='blue',label='AIMD RDF H-O')
plt.plot(r_lmp_HO,gr_lmp_HO,color='blue',label='Lammps RDF H-O',linestyle=':')
plt.title('RDF H-O AIMD vs Lammps DPFF '+model_name,fontsize=16)
plt.xlabel('r (A)',fontsize=14)
plt.ylabel('g(r) ',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('rdf_comp/rdf_H-O')


# Read H-H gr data from both simulations 
r_HH = rdf_cp2k_2kmod_HH[:,0]
gr_HH = rdf_cp2k_2kmod_HH[:,1]
r_lmp_HH = rdf_lmp_2kmod_HH[:,0]
gr_lmp_HH = rdf_lmp_2kmod_HH[:,1]


#PLot and compare rdf from AIMD and Lammps 
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(r_HH,gr_HH,color='red',label='AIMD RDF H-H')
plt.plot(r_lmp_HH,gr_lmp_HH,color='red',label='Lammps RDF H-H',linestyle=':')
plt.title('RDF H-H AIMD vs Lammps DPFF '+model_name,fontsize=16)
plt.xlabel('r (A)',fontsize=14)
plt.ylabel('g(r) ',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('rdf_comp/rdf_H-H')


# Read O-O gr data from both simulations 
r_OO = rdf_cp2k_2kmod_OO[:,0]
gr_OO = rdf_cp2k_2kmod_OO[:,1]
r_lmp_OO = rdf_lmp_2kmod_OO[:,0]
gr_lmp_OO = rdf_lmp_2kmod_OO[:,1]


#PLot and compare rdf from AIMD and Lammps 
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(r_OO,gr_OO,color='green',label='AIMD RDF O-O')
plt.plot(r_lmp_OO,gr_lmp_OO,color='green',label='Lammps RDF O-O',linestyle=':')
plt.title('RDF O-O AIMD vs Lammps DPFF '+model_name,fontsize=16)
plt.xlabel('r (A)',fontsize=14)
plt.ylabel('g(r) ',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('rdf_comp/rdf_O-O')


# PLot the three rdf in the same plot 
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(r_HO,gr_HO,color='blue',label='AIMD RDF H-O')
plt.plot(r_lmp_HO,gr_lmp_HO,color='blue',label='Lammps RDF H-O',linestyle=':')
plt.plot(r_HH,gr_HH,color='red',label='AIMD RDF H-H')
plt.plot(r_lmp_HH,gr_lmp_HH,color='red',label='Lammps RDF H-H',linestyle=':')
plt.plot(r_OO,gr_OO,color='green',label='AIMD RDF O-O')
plt.plot(r_lmp_OO,gr_lmp_OO,color='green',label='Lammps RDF O-O',linestyle=':')
plt.title('RDF Comparisson AIMD vs Lammps DPFF '+model_name,fontsize=16)
plt.xlabel('r (A)',fontsize=14)
plt.ylabel('g(r) ',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('rdf_comp/rdf_full')


print('Plots for analysis performed sucessfully')