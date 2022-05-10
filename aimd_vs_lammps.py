import pandas as pd
import numpy as np
import lammps_logfile
import matplotlib.pyplot as plt
import os 

#Define the output files
lmp_output = 'mod_5k_NVT_0.5fs_2.5ps.log'
cp2k_ener_output = 'DPtry2_330_5K-1.ener'

# Define the name of the model 
steps_in_model = 5000
model_name = ' (Model 5K) \n'

#Create file to store outputs 
path = os.getcwd()
try:
    os.mkdir(path+"/analysis_output")
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)


# Read lammps input files and obtain all the information in it
lmp_2kdp = lammps_logfile.File(lmp_output)
lmp_2k_time = lmp_2kdp.get('Time')
lmp_2k_temp = lmp_2kdp.get('Temp')
lmp_2k_step = lmp_2kdp.get('Step')
lmp_2k_press = lmp_2kdp.get('Press')    #bar
lmp_2k_dens = lmp_2kdp.get('Density')   #g/cm^3
lmp_2k_toteng = lmp_2kdp.get('TotEng')  #eV
lmp_2k_kineng = lmp_2kdp.get('KinEng')
lmp_2k_poteng = lmp_2kdp.get('PotEng')    


# Plot the Pressure Distribution of the Lammps Simulation
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(lmp_2k_step,lmp_2k_press, color='r')
plt.title('Lammps DPFF Pressure Distribution'+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Pressure (bar)',fontsize=14)
plt.savefig('analysis_output/lmp_2kmod_Press')


# Plot the Desnisity Distribution of the Lammps Simulation
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(lmp_2k_step,lmp_2k_dens, color='r')
plt.title('Lammps DPFF Density Distribution'+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Density (g/cm^3)',fontsize=14)
plt.savefig('analysis_output/lmp_2kmod_Density')


# Open CP2K log file 
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
lmp_2k_toteng_ave = np.average(lmp_2k_toteng)
lmp_2k_toteng_ave = round(lmp_2k_toteng_ave,3)


#Determine the Error % between the total Energy values 
error_totEng = 100 * (cp2k_totEng_ave-lmp_2k_toteng_ave)/cp2k_totEng_ave
error_totEng = abs(round(error_totEng,4))


# Compare Total energy of the system from CP2k and lammps in eV
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(cp2k_steps,cp2k_totEng_eV, color='g', label='AIMD Average Total Energy = {} eV'.format(cp2k_totEng_ave))
plt.plot(lmp_2k_step,lmp_2k_toteng, color='blue', label='Lammps DPFF  Average Total Energy = {} eV'.format(lmp_2k_toteng_ave))
plt.hlines(cp2k_totEng_ave,color='red',xmin=0, xmax=steps_in_model,label='AIMD TotE = {} eV'.format(round(cp2k_totEng_ave,4)))
plt.hlines(lmp_2k_toteng_ave,color='yellow',xmin=0, xmax=steps_in_model,label='Lammps KE = {} eV'.format(round(lmp_2k_toteng_ave,4)))
plt.plot([],[],label='Error = {} %'.format(error_totEng))
plt.title('AIMD vs Lammps DPFF Total Energy Distributions'+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Total Energy of the system (eV)',fontsize=14)
plt.legend(fontsize=14,loc='upper right')
plt.savefig('analysis_output/cp2k_vs_Lammps_TotEng_eV')


#Back calculate TotEng in Hartree units
lmp_2k_toteng_ht = lmp_2k_toteng / 27.2114
cp2k_totEng_ht = cp2k_totEng_eV / 27.2114


# Compare Total energy of the system from CP2k and lammps in Ht
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(cp2k_steps,cp2k_totEng_ht, color='g', label='AIMD Average Total Energy ')
plt.plot(lmp_2k_step,lmp_2k_toteng_ht, color='b', label='Lammps DPFF  Average Total Energy')
plt.hlines(np.average(cp2k_totEng_ht),color='red',xmin=0, xmax=steps_in_model,label='AIMD PE = {} Ht'.format(round(np.average(cp2k_totEng_ht),4)))
plt.hlines(np.average(lmp_2k_toteng_ht),color='yellow',xmin=0, xmax=steps_in_model,label='Lammps PE = {} Ht'.format(round(np.average(lmp_2k_toteng_ht),4)))
plt.title('AIMD vs Lammps DPFF Total Energy Distributions (Ht)'+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Total Energy of the system (Hartree)',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('analysis_output/cp2k_vs_Lammps_TotEng_Ht')


# Determine tem average from cp2k and lammps 
cp2k_T_ave = np.average(cp2k_Temp)
cp2k_T_ave = round(cp2k_T_ave,2)
lmp_T_ave = np.average(lmp_2k_temp)
lmp_T_ave = round(lmp_T_ave,2)


#Determine the error in the average temoeratures 
error_temp = 100 * (cp2k_T_ave - lmp_T_ave)/cp2k_T_ave
error_temp = abs(round(error_temp,4))


#Pot the Temperature ditribution of both simulations
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(cp2k_steps,cp2k_Temp, color='g', label='AIMD')
plt.plot(lmp_2k_step,lmp_2k_temp, color='b',label='Lammps')
plt.hlines(cp2k_T_ave,color='r',xmin=0, xmax=steps_in_model,label='AIMD Temperature {} K'.format(cp2k_T_ave),linewidth=4)
plt.hlines(lmp_T_ave,color='yellow',xmin=0, xmax=steps_in_model,label='Lammps Temperature = {} K'.format(lmp_T_ave),linewidth=4)
plt.plot([],[],label='Error = {} %'.format(error_temp))
plt.title('CP2K vs Lammps DP Temperature Distribution '+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Temperature of the system (K)',fontsize=14)
plt.legend(fontsize=14,loc='upper left')
plt.savefig('analysis_output/cp2k_vs_Lammps_Temp')


#Determine the average KE for both simulations and determine the error%
cp2k_kinE_eV_ave = np.average(cp2k_kinE_eV)
lmp_2k_kineng_ave =np.average(lmp_2k_kineng)
error_kinEng = 100 * (cp2k_kinE_eV_ave-lmp_2k_kineng_ave)/cp2k_kinE_eV_ave
error_kinEng = abs(round(error_kinEng,4))


# Plot and compare the KE 
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(cp2k_steps,cp2k_kinE_eV, color='g', label='AIMD')
plt.plot(lmp_2k_step,lmp_2k_kineng, color='blue',label='Lammps')
plt.hlines(cp2k_kinE_eV_ave,color='red',xmin=0, xmax=steps_in_model,label='AIMD KE = {} eV'.format(round(cp2k_kinE_eV_ave,4)))
plt.hlines(lmp_2k_kineng_ave,color='yellow',xmin=0, xmax=steps_in_model,label='Lammps KE = {} eV'.format(round(lmp_2k_kineng_ave,4)))
plt.plot([],[],label='Error = {} %'.format(error_kinEng))
plt.title('AIMD vs Lammps DPFF Kinetic Energy Distributions'+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Total Energy of the system (eV)',fontsize=14)
plt.legend(fontsize=14,loc='upper left')
plt.savefig('analysis_output/cp2k_vs_Lammps_KinEng')


#Determine the average KE for both simulations and determine the error%
cp2k_potE_eV_ave = np.average(cp2k_potE_eV)
lmp_2k_poteng_ave = np.average(lmp_2k_poteng)
error_potEng = 100 * (cp2k_potE_eV_ave-lmp_2k_poteng_ave)/cp2k_potE_eV_ave
error_potEng = abs(round(error_potEng,4))


#PLot and compare the PE
plt.figure(figsize=(12,9),facecolor='white')
plt.plot(lmp_2k_step,lmp_2k_poteng, color='blue',label='Lammps')
plt.plot(cp2k_steps,cp2k_potE_eV,color='g',label='AIMD')
plt.hlines(cp2k_potE_eV_ave,color='red',xmin=0, xmax=steps_in_model,label='AIMD PE = {} eV'.format(round(cp2k_potE_eV_ave,4)))
plt.hlines(lmp_2k_poteng_ave,color='yellow',xmin=0, xmax=steps_in_model,label='Lammps PE = {} eV'.format(round(lmp_2k_poteng_ave,4)))
plt.plot([],[],label='Error = {} %'.format(error_potEng),color='white')
plt.title('AIMD vs Lammps DPFF Potential Energy Distribution '+model_name,fontsize=16)
plt.xlabel('Step',fontsize=14)
plt.ylabel('Total Energy of the system (eV)',fontsize=14)
plt.legend(fontsize=14)
plt.savefig('analysis_output/cp2k_vs_Lammps_PotEng')


print('Plots for analysis performed sucessfully')