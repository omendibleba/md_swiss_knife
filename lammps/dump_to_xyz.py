#! /usr/bin/env python3

import numpy as np
from copy import deepcopy
import argparse

parser = argparse.ArgumentParser(description='Read log and dump fle from lammps simulation and creates training and test data sets in npz format.')
#parser.add_argument('log_file_name', help='The name of the LAMMPS log file')
parser.add_argument('forces', help='The name of the LAMMPS forces.dump file')
parser.add_argument('--output','-o',help='Name of the output xyz file.')


args = parser.parse_args()

# # Read the forces file with ase from the lmp nnip simulation 
# filename = '../but1_box100_T600K/forces.dump'


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

# Extract the timestep numbers
timesteps = sorted(data.keys())


# Write the xyz file
with open(args.output, "w") as f:
    # Iterate over the timesteps
    for ts in timesteps:
        # Get the number of atoms
        f.write(str(data[ts]['num_atoms']) + "\n")
        
        # Write the timestep
        f.write("Atoms. Timestep: {} \n".format(ts))

        # Get the atoms tyoe and coordinate array
        for atom in data[ts]['atoms']:
            f.write("{} {} {} {}\n".format(int(atom[1]), atom[2], atom[3], atom[4]))

print('xyz file created succesfully! Thank You!')
