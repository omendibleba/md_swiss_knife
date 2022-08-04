## This script creates plot to visualize Potential , knetic energy, Temperature,etc, /
#from the energy file from cp2k aimd. 


#Import modules 
import numpy as np
import matplotlib.pyplot as plt
import os 


#Define the output files
cp2k_ener_output = 'Molten_108NaCl-1.ener'


# Create folder to store created plots.
path = os.getcwd()
try:
    os.mkdir(path+"/analysis_output")
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)


# Load CP2K ener file 
cp2k_out = np.loadtxt(cp2k_ener_output)

# Extract Energy and Temperature information from CP2k output file.
# REMEMBER THESE ENERGIES ARE IN HARTREE
cp2k_steps = cp2k_out[:, 0]
cp2k_time  = cp2k_out[:,1]
cp2k_kinE  = cp2k_out[:,2]
cp2k_Temp  = cp2k_out[:,3]
cp2k_potE  = cp2k_out[:,4]


## Change the Units of the KE and PE from Hartree to eV. 1 Ht - 27.2114 eV
cp2k_kinE_eV = cp2k_kinE * 27.2114
cp2k_potE_eV = cp2k_potE * 27.2114


# Add the KE and PE to determine the total Energy of the system
cp2k_totEng_eV = np.add(cp2k_kinE_eV,cp2k_potE_eV)


# Determine the average of the total energy from both simulations
cp2k_totEng_ave = np.average(cp2k_totEng_eV)
cp2k_totEng_ave = round(cp2k_totEng_ave,3)


## Plot total energy 

# Compare Total energy of the system from CP2k and lammps in eV
plt.figure(figsize=(9,6),facecolor='white')
plt.plot(cp2k_time,cp2k_totEng_eV, color='g') #label='AIMD Average Total Energy = {} eV'.format(cp2k_totEng_ave))
plt.hlines(cp2k_totEng_ave,color='red',xmin=0, xmax=max(cp2k_steps),label='AIMD TotE = {} eV'.format(round(cp2k_totEng_ave,4)))
#plt.plot([],[],label='Error = {} %'.format(error_totEng))
plt.title('AIMD Total Energy Distribution',fontsize=16)
plt.xlabel('Time (fs)',fontsize=14)
plt.ylabel('Total Energy of the system (eV)',fontsize=14)
plt.legend(fontsize=14,loc='upper right')
plt.savefig('analysis_output/aimd_TotEng_eV',dpi=500)


##Temperature

# Determine tem average from cp2k 
cp2k_T_ave = np.average(cp2k_Temp)
cp2k_T_ave = round(cp2k_T_ave,2)


#Pot the Temperature ditribution of both simulations
plt.figure(figsize=(9,6),facecolor='white')
plt.plot(cp2k_time,cp2k_Temp, color='g')
plt.hlines(cp2k_T_ave,color='r',xmin=0, xmax=max(cp2k_steps),label='AIMD Temperature {} K'.format(cp2k_T_ave),linewidth=4)
plt.title('CP2K Temperature Distribution ',fontsize=16)
plt.xlabel('Time (fs)',fontsize=14)
plt.ylabel('Temperature of the system (K)',fontsize=14)
plt.legend(fontsize=14,loc='upper left')
plt.savefig('analysis_output/aimd_Temp')


##Potential Energy

#Determine the average KE for both simulations and determine the error%
cp2k_potE_eV_ave = round(np.average(cp2k_potE_eV),2)

#PLot and compare the PE
plt.figure(figsize=(9,6),facecolor='white')
plt.plot(cp2k_time,cp2k_potE_eV,color='g')
plt.hlines(cp2k_potE_eV_ave,color='red',xmin=0, xmax=max(cp2k_steps),label='AIMD PE = {} eV'.format(round(cp2k_potE_eV_ave,4)))
#plt.plot([],[],label='Error = {} %'.format(error_potEng),color='white')
plt.title('AIMD Potential Energy Distribution ',fontsize=16)
plt.xlabel('Time (fs)',fontsize=14)
plt.ylabel('Total Energy of the system (eV)',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('analysis_output/aimd_PotEng')


#Kinetic Energy 

#Determine the average KE for both simulations and determine the error%
cp2k_kinE_eV_ave = np.average(cp2k_kinE_eV)

# Plot and compare the KE 
plt.figure(figsize=(9,6),facecolor='white')
plt.plot(cp2k_time,cp2k_kinE_eV, color='g')
plt.hlines(cp2k_kinE_eV_ave,color='red',xmin=0, xmax=max(cp2k_steps),label='AIMD KE = {} eV'.format(round(cp2k_kinE_eV_ave,4)))
#plt.plot([],[],label='Error = {} %'.format(error_kinEng))
plt.title('AIMD Kinetic Energy Distributions',fontsize=16)
plt.xlabel('Time (fs)',fontsize=14)
plt.ylabel('Total Energy of the system (eV)',fontsize=14)
plt.legend(fontsize=14,loc='upper left')
plt.savefig('analysis_output/aimd_KinEng')

print('Plots for analysis performed sucessfully')