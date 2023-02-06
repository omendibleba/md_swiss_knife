#! /usr/bin/env python3
import numpy as np
from copy import deepcopy
import argparse



# Define parser 
parser = argparse.ArgumentParser(description='MOdify atom type array in npz file created from lmpdump_to_npz.py')
parser.add_argument('npz', type=str, help='npz file to modify')
parser.add_argument('dumpfile', type=str, help='Original dump file from which npz file was created')

# finish parser 
args = parser.parse_args()



filename = args.dumpfile

#load npz file
npz = npz = np.load(args.npz)


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
data = parse_lammpstrj(filename=args.dumpfile)


data[0]

# Determine the values of the keys ofrom the given start 
keys = list(data.keys())
last500_keys = keys[500:]
#last500_keys

# copy the last 500 timesteps into a new dictionary
last500 = {}
for key in last500_keys:
    last500[key] = data[key]



# Fot the atom type array 

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


#type_atom_num

#
for i in range(len(data_copy[0]['atoms'])):

    print(data_copy[0]['atoms'][i])
    # #print(data_copy[0]['atoms'][i])    
    if data_copy[0]['atoms'][i] == 1.0:

        type_atom_num[i] = int(1)

    elif data_copy[0]['atoms'][i] == 2.0:

        type_atom_num[i] = int(8)

    elif data_copy[0]['atoms'][i] == 3.0:

        type_atom_num[i] = int(11)

    elif data_copy[0]['atoms'][i] == 4.0:

        type_atom_num[i] = int(17)

#type_atom_num

#
# Save it with the new type atom array 
print("Saving npz file with new atom type array")
np.savez(args.npz, R=npz['R'], F=npz['F'], z=type_atom_num, E=npz['E'])

# 
print("All done! Thank You!")


