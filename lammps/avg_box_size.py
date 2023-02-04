#! /usr/bin/env python3
""""
THis script tackes the log file of an NPT Lammps simulation as input and takes the Lx,Lyand Lz, columnsfrom it. 
THen calcultest the average box size based on a given amount of frames  and prints it to the screen.
"""

import argparse
import numpy as np
import lammps_logfile

parser = argparse.ArgumentParser(description='Plot the temperature from a LAMMPS log file')
parser.add_argument('log_file_name', help='The name of the LAMMPS log file')
parser.add_argument('-v','--volume',default=True,help='If true, the volume of the box is taken form the log file',action='store_false')

parser.add_argument('-s', '--start', type=int, default=-500, help='The starting frame to plot')

args = parser.parse_args()


#read log file
log = lammps_logfile.File(args.log_file_name)

if args.volume:

    # Read time and volume 
    time = log.get("Time")
    vol = log.get("Volume")

    # Calculate the avergae volume from start to the end
    vol_ave = np.average(vol[args.start:])

    #Print the average volume
    print('The average volume is ', vol_ave, ' Angstroms^3 \n')

     # Caclculate the cubic root of the average volume to obtain the ave length of each side of the box
    box_ave = vol_ave**(1/3)

    # Print the average length of the box sides 
    print('The average box size length is ', box_ave, ' Angstroms \n')


else:
    #REad values of interest
    step = log.get("Step") ## Read steps
    time = log.get("Time")
    lx = log.get("Lx")
    ly = log.get("Ly")
    lz = log.get("Lz")

    # Calculate the average of the array from start to the end
    lx_ave = np.average(lx[args.start:])
    ly_ave = np.average(ly[args.start:])
    lz_ave = np.average(lz[args.start:])

    # Print the average volume of the box 
    print('The average volume is ', lx_ave*ly_ave*lz_ave, ' Angstroms^3 \n')

    # Print the average length of the box in each axis 
    print('The average box size in the x direction is ', lx_ave, ' Angstroms')
    print('The average box size in the y direction is ', ly_ave, ' Angstroms')
    print('The average box size in the z direction is ', lz_ave, ' Angstroms')
 