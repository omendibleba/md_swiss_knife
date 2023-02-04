#! /usr/bin/env python3
""""
In this script, argparse is used to parse command-line arguments. 
The parser.add_argument() method adds two arguments: log_file_name, which is a required argument, and -s or --start, which is an optional argument with a default value of -500. 
The script then uses the args object to retrieve the values of the log_file_name and start arguments. 
To run this script from the terminal, use the command python script.py log.lammps -s 100 to plot the temperature from the file log.lammps starting from frame 100.
"""

import argparse
import numpy as np
import matplotlib.pyplot as plt
import lammps_logfile

parser = argparse.ArgumentParser(description='Plot the temperature from a LAMMPS log file')
parser.add_argument('log_file_name', help='The name of the LAMMPS log file')
parser.add_argument('ensemble', help='Specifuy Simulation Ensemble (i.e.g, NVT, NPT, etc.')
parser.add_argument('-s', '--start', type=int, default=-500, help='The starting frame to plot')
parser.add_argument('-t', '--title', default='Temperature Plot', help='The title for the plot')


args = parser.parse_args()


#If statemnt to check if the ensemble is NVT or NPT
if args.ensemble == 'NVT':
        
    #read log file
    log = lammps_logfile.File(args.log_file_name)

    # REad values of interest 
    #step = log.get("Step") ## Read steps
    time = log.get("Time")
    temp = log.get("Temp")
    press = log.get("Press")
    potEng = log.get("PotEng")
    kinEng = log.get("KinEng")

    # Determine the length of the arrays 
    n = len(time[args.start:])
    print(' The number of frames is ', n)

    # # Temperature average
    temp_ave = round(np.average(temp[args.start:]),2)

    # # Fro pressure
    press_ave = round(np.average(press[args.start:]),4)


    # # For Potential ENergy 
    potEng_ave = round(np.average(potEng[args.start:]),3)


    # # For the Kinetic ENergy 
    kinEng_ave = round(np.average(kinEng[args.start:]),3)



    # Create a single figura that include the four plots in two columns and two rows 

    fig, axs = plt.subplots(2, 2,figsize=(10,10))
    fig.suptitle('LAMMPS log file Analysis: '+str(args.title),fontsize=16 , fontweight='bold')
    axs[0, 0].plot(time[args.start:],temp[args.start:],color="blue")
    axs[0, 0].hlines(temp_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Temperature = {} K".format(temp_ave))
    axs[0, 0].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[0, 0].set_ylabel("Temperature (K)",fontsize=16 , fontweight='bold')
    axs[0, 0].tick_params(axis='both', which='major', labelsize=12)
    axs[0, 0].legend(fontsize=12)

    axs[0, 1].plot(time[args.start:],press[args.start:],color="blue")
    axs[0, 1].hlines(press_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Ave Pressure = {} atm".format(press_ave))
    axs[0, 1].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[0, 1].set_ylabel("Pressure (atm)",fontsize=16 , fontweight='bold')
    axs[0, 1].tick_params(axis='both', which='major', labelsize=12)
    axs[0, 1].legend(fontsize=12)

    axs[1, 0].plot(time[args.start:],potEng[args.start:],color="blue")
    axs[1, 0].hlines(potEng_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Ave Potential Energy = {} Kcal/mol".format(potEng_ave))
    axs[1, 0].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[1, 0].set_ylabel("Potential Energy (Kcal/mol)",fontsize=16 , fontweight='bold')
    axs[1, 0].tick_params(axis='both', which='major', labelsize=12)
    axs[1, 0].legend(fontsize=12,loc='lower right')

    axs[1, 1].plot(time[args.start:],kinEng[args.start:],color="blue")
    axs[1, 1].hlines(kinEng_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Ave Kinetic Energy = {} Kcal/mol ".format(kinEng_ave ))
    axs[1, 1].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[1, 1].set_ylabel("Kinetic Energy (Kcal/mol)",fontsize=16 , fontweight='bold')
    axs[1, 1].tick_params(axis='both', which='major', labelsize=12)
    axs[1, 1].legend(fontsize=12)

    plt.tight_layout()
    # replace empty spcae in args.title and replace with _
    
    plt.savefig(args.title.replace(" ","_")+'.png',dpi=300 )
    plt.show()

elif args.ensemble == 'NPT':

    #read log file
    log = lammps_logfile.File(args.log_file_name)

    # REad values of interest 
    #step = log.get("Step") ## Read steps
    time = log.get("Step")
    temp = log.get("Temp")
    density = log.get("Density")
    potEng = log.get("PotEng")
    kinEng = log.get("KinEng")

    # Determine the length of the arrays 
    n = len(time[args.start:])
    print(' The number of frames is ', n)

    # # Temperature average
    temp_ave = round(np.average(temp[args.start:]),2)

    # # Fro pressure
    press_ave = round(np.average(density[args.start:]),4)


    # # For Potential ENergy 
    potEng_ave = round(np.average(potEng[args.start:]),3)


    # # For the Kinetic ENergy 
    kinEng_ave = round(np.average(kinEng[args.start:]),3)



    # Create a single figura that include the four plots in two columns and two rows 

    fig, axs = plt.subplots(2, 2,figsize=(10,10))
    fig.suptitle('LAMMPS log file Analysis: '+str(args.title),fontsize=16 , fontweight='bold')
    axs[0, 0].plot(time[args.start:],temp[args.start:],color="blue")
    axs[0, 0].hlines(temp_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Temperature = {} K".format(temp_ave))
    axs[0, 0].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[0, 0].set_ylabel("Temperature (K)",fontsize=16 , fontweight='bold')
    axs[0, 0].tick_params(axis='both', which='major', labelsize=12)
    axs[0, 0].legend(fontsize=12)

    axs[0, 1].plot(time[args.start:],density[args.start:],color="blue")
    axs[0, 1].hlines(press_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Ave Density = {} $g/cm^3$".format(press_ave))
    axs[0, 1].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[0, 1].set_ylabel("Density $(g/cm^3)$",fontsize=16 , fontweight='bold')
    axs[0, 1].tick_params(axis='both', which='major', labelsize=12)
    axs[0, 1].legend(fontsize=12)

    axs[1, 0].plot(time[args.start:],potEng[args.start:],color="blue")
    axs[1, 0].hlines(potEng_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Ave Potential Energy = {} Kcal/mol".format(potEng_ave))
    axs[1, 0].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[1, 0].set_ylabel("Potential Energy (Kcal/mol)",fontsize=16 , fontweight='bold')
    axs[1, 0].tick_params(axis='both', which='major', labelsize=12)
    axs[1, 0].legend(fontsize=12,loc='lower right')

    axs[1, 1].plot(time[args.start:],kinEng[args.start:],color="blue")
    axs[1, 1].hlines(kinEng_ave,xmin=min(time[args.start:]),xmax=max(time),color="red",label = "Ave Kinetic Energy = {} Kcal/mol ".format(kinEng_ave ))
    axs[1, 1].set_xlabel("Time (ps)",fontsize=16 , fontweight='bold')
    axs[1, 1].set_ylabel("Kinetic Energy (Kcal/mol)",fontsize=16 , fontweight='bold')
    axs[1, 1].tick_params(axis='both', which='major', labelsize=12)
    axs[1, 1].legend(fontsize=12)


    plt.tight_layout()
    plt.savefig(args.title.replace(" ","_")+'.png',dpi=300 )
    plt.show()


