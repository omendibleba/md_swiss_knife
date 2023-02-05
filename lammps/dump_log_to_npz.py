#! /usr/bin/env python3
""" 
Script to Generate npz file requirex for nequip trianing .
Is read the dup file and log file from lammps simulation and generate npz file

Usage:
    dump_log_to_npz.py <dump_file> <log_file> <npz_file>

thremo_style requires the following format. : 
dump myDump all custom 4000 forces.dump id type x y z fx fy fz


"""

# Import libraries 
import numpy as np
from copy import deepcopy
import lammps_logfile as lmplog
import argparse
    
# Define dump file or trajectory file and the log file 

# Define ther parser and argument inputs 
parser = argparse.ArgumentParser(description='Generate npz file from lammps dump and log file')
parser.add_argument('log_file', help='The name of the log file')
parser.add_argument('dump_file', help='The name of the dump file')
parser.add_argument('-n','--npz_file',default='npz_data', help='The name of the npz file')
args = parser.parse_args()


filename = args.dump_file
logfile = args.log_file

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
data = parse_lammpstrj(filename)


# Define function that creates array of coordinates 
def create_array_of_coordinates(filename):

    data = parse_lammpstrj(filename=filename)
    data_copy = deepcopy(data)
    for ts in data_copy:
        #data_copy[ts]['atoms'] = [ atom[1:4] for atom in data[ts]['atoms']]
        data_copy[ts]['atoms'] = [ atom[2:5] for atom in data[ts]['atoms']]

        
    # Get the number of frames
    num_frames = len(data_copy)

    # Get the number of atoms in the first frame (assuming all frames have the same number of atoms)
    num_atoms = len(data_copy[list(data_copy.keys())[0]]['atoms'])

    # Create a new empty array with the desired shape
    coordinates = np.empty((num_frames, num_atoms, 3))

    # Iterate over the dictionary and fill the array with the coordinates
    for i, (ts, atom_data) in enumerate(data_copy.items()):
        coordinates[i, :, :] = atom_data['atoms']
        
    return coordinates

# Use the function to create the array of coordinates
coordinates = create_array_of_coordinates(filename=filename)



# Define function that creates array of forces
# Define function to create array of force 

def create_array_of_forces(filename):

    data = parse_lammpstrj(filename=filename)
    data_copy = deepcopy(data)
    for ts in data_copy:
        #data_copy[ts]['atoms'] = [ atom[1:4] for atom in data[ts]['atoms']]
        data_copy[ts]['atoms'] = [ atom[5:8] for atom in data[ts]['atoms']]

        
    # Get the number of frames
    num_frames = len(data_copy)

    # Get the number of atoms in the first frame (assuming all frames have the same number of atoms)
    num_atoms = len(data_copy[list(data_copy.keys())[0]]['atoms'])

    # Create a new empty array with the desired shape
    forces = np.empty((num_frames, num_atoms, 3))

    # Iterate over the dictionary and fill the array with the forces
    for i, (ts, atom_data) in enumerate(data_copy.items()):
        forces[i, :, :] = atom_data['atoms']
        
    return forces

# Use the function to create the array of forces
forces = create_array_of_forces(filename=filename)



# Define function that creates array of energies from log file 
def parse_lmp_log_etotal(logfile):

    # Parse the log file
    log = lmplog.File(logfile)

    # Extract the total energy
    etotal = log.get('PotEng')

    # Convert the data to a numpy array
    etotal = np.array(etotal)

    return etotal

# Use the function to create the array of energies
etotal = parse_lmp_log_etotal(logfile=logfile)


# Define function that generates Array of types
## Define functoin that Create array of z (types) using the code from above 


def create_array_of_types(filename):

    data = parse_lammpstrj(filename=filename)
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
        if data_copy[0]['atoms'][i] == 1.0 or 3.0:

            type_atom_num[i] = int(1)

        elif data_copy[0]['atoms'][i] == 2.0 or 4.0:

            type_atom_num[i] = int(6)
    
    return type_atom_num

# Use the function to create the array of types
type_atom_num = create_array_of_types(filename=filename)



## Save arrays into .npz format

np.savez(str(args.npz_file).replace(' ','_')+'.npz', R=coordinates, F=forces, z=type_atom_num, E=etotal)

print('Files in .npz format were saved successfully! Thanks!!')
