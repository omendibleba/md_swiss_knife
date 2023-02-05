#! /usr/bin/env python3
# Import libraries 
import argparse
import numpy as np
from copy import deepcopy
import lammps_logfile as lmplog


# Define dump file or trajectory file and the log file 
# filename = 'but1_box100_T600K/forces.dump'
# logfile = 'but1_box100_T600K/log.lammps'
# start = -500
# n_training = 400 

parser = argparse.ArgumentParser(description='Read log and dump fle from lammps simulation and creates training and test data sets in npz format.')
parser.add_argument('log_file_name', help='The name of the LAMMPS log file')
parser.add_argument('forces', help='The name of the LAMMPS forces.dump file')
parser.add_argument('-s', '--start', type=int, default=-500, help='The starting frame. Also defines the number of frames.')
parser.add_argument('-t', '--training', default=500, help='Number of frames to be included iin the training set ')
parser.add_argument('-c', '--complete', default=False, help='Wehter or of not you want to create an npz of the whole trajectory.',action='store_true')
args = parser.parse_args()

# Define function that parses into diictionary
def parse_lammpstrj(filename):

    import re
    """Parse a LAMMPS trajectory file into a dictionary.

    Parameters
    ----------
    filename : str
        The name of the LAMMPS trajectory file.

    Returns
    -------
    data : dict
        A dictionary containing the data from the LAMMPS trajectory file.

    """
    # Initialize the data dictionary
    data = {}

    # Open the file
    with open(filename, 'r') as f:
        # Read the file line by line
        for line in f:
            # Check if the line starts with 'ITEM: TIMESTEP'
            if line.startswith('ITEM: TIMESTEP'):
                # Extract the timestep number
                timestep = int(next(f))
                data[timestep] = {}
            # Check if the line starts with 'ITEM: NUMBER OF ATOMS'
            elif line.startswith('ITEM: NUMBER OF ATOMS'):
                # Extract the number of atoms
                num_atoms = int(next(f))
                data[timestep]['num_atoms'] = num_atoms
            # Check if the line starts with 'ITEM: BOX BOUNDS'
            elif line.startswith('ITEM: BOX BOUNDS'):
                # Extract the box bounds
                box_bounds = [float(x) for x in re.findall(r'-?\d+\.\d+', next(f))]
                data[timestep]['box_bounds'] = box_bounds
            # Check if the line starts with 'ITEM: ATOMS'
            elif line.startswith('ITEM: ATOMS'):
                # Initialize the atoms list
                atoms = []
                # Read the rest of the lines in the block
                for _ in range(num_atoms):
                    # Split the line by ' ' and extract the values
                    values = [float(x) for x in next(f).split()]
                    atoms.append(values)
                # Add the atoms list to the data dictionary
                data[timestep]['atoms'] = atoms

        return data

# Use the function to parse the LAMMPS trajectory file
data = parse_lammpstrj(args.forces)

# Determine the values of the keys ofrom the given start 
keys = list(data.keys())
last500_keys = keys[args.start:]
#last500_keys

# copy the last 500 timesteps into a new dictionary
last500 = {}
for key in last500_keys:
    last500[key] = data[key]


# Create array of coordinates
for ts in last500:
    #last500[ts]['atoms'] = [ atom[1:4] for atom in data[ts]['atoms']]
    last500[ts]['atoms'] = [ atom[2:5] for atom in data[ts]['atoms']]
# Create array of coordinates based on the last 500 timesteps

# Get the number of frames
num_frames = len(last500)
print('The number of frames is: ',num_frames)

# Get the number of atoms in the first frame (assuming all frames have the same number of atoms)
num_atoms = len(last500[list(last500.keys())[0]]['atoms'])
print('The number of atoms is: ',num_atoms)


# Create a new empty array with the desired shape
coordinates = np.empty((num_frames, num_atoms, 3))

# Iterate over the dictionary and fill the array with the coordinates
for i, (ts, atom_data) in enumerate(last500.items()):
    coordinates[i, :, :] = atom_data['atoms']


# Create array of forces
data = parse_lammpstrj(filename=args.forces)
data2 = deepcopy(data)
# copy the last 500 timesteps into a new dictionary
last500_2 = {}
for key in last500_keys:
    last500_2[key] = data2[key]



for ts in last500_2:
    #last500[ts]['atoms'] = [ atom[1:4] for atom in data[ts]['atoms']]
    last500_2[ts]['atoms'] = [ atom[5:8] for atom in data2[ts]['atoms']]
# Create array of coordinates based on the last 500 timesteps

# Get the number of frames
num_frames = len(last500_2)
print('The number of frames is: ',num_frames)

# Get the number of atoms in the first frame (assuming all frames have the same number of atoms)
num_atoms = len(last500_2[list(last500_2.keys())[0]]['atoms'])
print('The number of atoms is: ',num_atoms)


# Create a new empty array with the desired shape
forces = np.empty((num_frames, num_atoms, 3))

# Iterate over the dictionary and fill the array with the coordinates
for i, (ts, atom_data) in enumerate(last500_2.items()):
    forces[i, :, :] = atom_data['atoms']

#forces[-1]
# # forces


# For the potential energy from the logfile 
# FOr the potential energy 

# Parse the log file
log = lmplog.File(args.log_file_name)

# Extract the total energy
poteng = log.get('PotEng')

# Convert the data to a numpy array
poteng = np.array(poteng)

# Extract the last 500 timesteps
poteng = poteng[args.start:]


# Fot the atoy type array 
data = parse_lammpstrj(filename=args.forces)
data_copy = deepcopy(data)
for ts in data_copy:
    #data_copy[ts]['atoms'] = [ atom[1:4] for atom in data[ts]['atoms']]
    data_copy[ts]['atoms'] = [ atom[1] for atom in data[ts]['atoms']]

    
# Get the number of frames
num_frames = len(data_copy)

# Get the number of atoms in the first frame (assuming all frames have the same number of atoms)
num_atoms = len(data_copy[list(data_copy.keys())[0]]['atoms'])

# Create a new empty array with the desired shape
type_atom_num = np.zeros((1, num_atoms))
type_atom_num  = type_atom_num.flatten()

for i in range(len(data_copy[0]['atoms'])):

    #print(data_copy[0]['atoms'][i])    
    if data_copy[0]['atoms'][i] == 1.0:

        type_atom_num[i] = int(6)

    elif data_copy[0]['atoms'][i] == 2.0:

        type_atom_num[i] = int(1)

type_atom_num

if args.complete == True:
    np.savez('but7_600KPE_last500_train.npz', R=coordinates, F=forces, z=type_atom_num, E=poteng)
# save the data in a file npz format 
else:
    np.savez('but7_600KPE_last500_train.npz', R=coordinates[:int(args.training)], F=forces[:int(args.training)], z=type_atom_num, E=poteng[:int(args.training)])
    np.savez('but7_600KPE_last500_test.npz', R=coordinates[int(args.training):], F=forces[int(args.training):], z=type_atom_num, E=poteng[int(args.training):])

print('Files created sucessfully!')
