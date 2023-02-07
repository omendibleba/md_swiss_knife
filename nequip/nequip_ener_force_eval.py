#! /usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
import ase
from ase.io import read
from sklearn.metrics import r2_score
import argparse



parser = argparse.ArgumentParser(description='Read the xyz file created from the nequip-evaluate command using -dataset-config and -output and compare it to the .npz file created from the lmpdump_to_npz.py script. \
    The script will create a scatter plot comparing the model predictiong vs the training/test data. The energies and forces  from the xyz file are from the model vs the energies and forces  from the .npz file and will also calculate the R2 value for the energies and forces .')
parser.add_argument('traj', help='Output from nequip-evaluate. Is an xyz file containing the energies and forces predicted by the model at any given configuration ')
parser.add_argument('test_data', help='The traiing or test data which includes the configurations that were given to the model for the evaluation. Is in npz format.')
parser.add_argument('--title','-t',default=' ', help='Title of the plot and for saved image. Default is None. ')

args = parser.parse_args()

# Gererate xyz file runing the following command 
# nequip-evaluate --dataset-config results/toluene_2/toluene_2/config.yaml --batch 50 --output test_2.xyz --model results/toluene_2/toluene_2/best_model.pth

# Read the trajectory using ase 
# traj = read('tol_clmd_eval_test.xyz', index=':')
#traj = read('but1_rc_2_testdata_eval.xyz', index=':')
traj = read(args.traj, index=':')
#test_data = np.load('toluene_t5_potEng.npz')
#test_data = np.load('../but7_600KPE_last500_test.npz')

# Read .npz file 
test_data = np.load(args.test_data)

# Determine the number of atoms 
natoms = len(test_data['z'])

# Create an array of zerow of length traj
energies = np.zeros(len(traj))

print('The number of evaluated configurations is ', len(traj))

# Create a for loop to read each of the energies from the trajectory file and store them in the array

for i in range(len(traj)):
    energies[i] = traj[i].get_potential_energy()



len(test_data['E'])

# Separate the energy from the training data
test_data_e = test_data['E']


#  Determinme the R2 value for the energies using numpy

r2 = r2_score(test_data_e, energies)


# Scatter plot of energies vs the energies from the .npz file
title= str(args.title)
#Define size of figure
# plt.figure(figsize=(9,6))

# plt.title(title+'NNIP-Predictions vs Test Data \n',fontsize=16,fontweight='bold')

# plt.scatter(energies, test_data_e)
# plt.plot(test_data_e, test_data_e, color='red')
# plt.plot([],[],' ',label='R2 = %0.4f' % r2)
# plt.xlabel('Test data PE (kcal/mol) ',fontsize=14,fontweight='bold')
# plt.ylabel(' NNIP-Predictions PE (kcal/mol) ',fontsize=14,fontweight='bold')


# plt.xticks(fontsize=11)
# plt.yticks(fontsize=11)

# plt.legend(fontsize=11,loc='upper left')

# plt.show()

# REad the forces from the .xyz file 

forces = np.zeros((len(traj), 14, 3))

for i in range(len(traj)):
    forces[i] = traj[i].get_forces()

# Define the prediction and test array of the forces in x, y, and z directions 

pred_fx = forces[:,:,0]
pred_fy = forces[:,:,1]
pred_fz = forces[:,:,2]

test_fx = test_data['F'][:,:,0]
test_fy = test_data['F'][:,:,1]
test_fz = test_data['F'][:,:,2]

# Determine r2 value for the forces in the x direction
r2_fx = r2_score(pred_fx, test_fx)
# Determine r2 value for the forces in the y direction
r2_fy = r2_score(pred_fy, test_fy)
# Determine r2 value for the forces in the z direction
r2_fz = r2_score(pred_fz, test_fz)

# Create a figure with four subplots, and the axes array is 2-d. The first row is for the eregy tha the force in x. the second row is for force in y and z 

fig, axs = plt.subplots(2, 2, figsize=(9,6))

# Add vertical and horizontal space between the subplots
fig.subplots_adjust(hspace=0.5, wspace=0.5)

# Add title to the figure
fig.suptitle(title+'\n',fontsize=16,fontweight='bold')

# Plot the predicted energies vs the test energies
axs[0, 0].scatter( test_data_e,energies)
axs[0, 0].plot(test_data_e, test_data_e, color='red')
axs[0, 0].plot([],[],' ',label='R2 = %0.6f' % r2)
axs[0, 0].set_title('Potential Energy ',fontsize=16,fontweight='bold')
axs[0, 0].set_xlabel('Test data (kcal/mol) ',fontsize=14,fontweight='bold')
axs[0, 0].set_ylabel(' NNIP-Predictions \n (kcal/mol) ',fontsize=14,fontweight='bold')
axs[0, 0].legend(fontsize=14,loc='upper left')

# Plot the predicted forces in the x direction vs the test forces in the x direction
axs[0, 1].scatter(test_fx, pred_fx)
axs[0, 1].plot(test_fx, test_fx, color='red')
axs[0, 1].plot([],[],' ',label='R2 = %0.6f' % r2_fx)
axs[0, 1].set_title(' Force x-axis ',fontsize=16,fontweight='bold')
axs[0, 1].set_xlabel('Test data (kcal/mol/Angstrom) ',fontsize=14,fontweight='bold')
axs[0, 1].set_ylabel(' NNIP-Predictions \n (kcal/mol/Angstrom) ',fontsize=14,fontweight='bold')
axs[0, 1].legend(fontsize=14,loc='upper left')

# Plot the predicted forces in the y direction vs the test forces in the y direction
axs[1, 0].scatter(test_fy, pred_fy)
axs[1, 0].plot(test_fy, test_fy, color='red')
axs[1, 0].plot([],[],' ',label='R2 = %0.6f' % r2_fy)
axs[1, 0].set_title('Force y-axis',fontsize=16,fontweight='bold')
axs[1, 0].set_xlabel('Test data (kcal/mol/Angstrom) ',fontsize=14,fontweight='bold')
axs[1, 0].set_ylabel(' NNIP-Predictions \n (kcal/mol/Angstrom) ',fontsize=14,fontweight='bold')
axs[1, 0].legend(fontsize=14,loc='upper left')

# Plot the predicted forces in the z direction vs the test forces in the z direction
axs[1, 1].scatter(test_fz, pred_fz)
axs[1, 1].plot(test_fz, test_fz, color='red')
axs[1, 1].plot([],[],' ',label='R2 = %0.6f' % r2_fz)
axs[1, 1].set_title('Force z-axis',fontsize=16,fontweight='bold')
axs[1, 1].set_xlabel('Test data (kcal/mol/Angstrom) ',fontsize=14,fontweight='bold')
axs[1, 1].set_ylabel(' NNIP-Predictions \n (kcal/mol/Angstrom) ',fontsize=14,fontweight='bold')
axs[1, 1].legend(fontsize=14,loc='upper left')


# Save the figure
plt.savefig(title.replace(' ','_')+ '.png', dpi=300, bbox_inches='tight')

plt.show()
