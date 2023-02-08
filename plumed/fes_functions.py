"""
Random funvtions to read colective variable data and plot histograms, probability density functions, and free energy surfaces and free energy 

Working on improving documentation. 
"""

import numpy as np 
import matplotlib.pyplot as plt
# NOw letrs re calculate the pdf but using a smoothing function
from scipy.ndimage.filters import gaussian_filter1d

## Example of loading data 
# # Load calculated dihedrals for butane molecule 
# dih_rc_10 = np.loadtxt('dihedrals.dat')

# Create af function to bin the data for later preparation of hisogram using bar chart

def bin_data(data, bins):
    """
    Bin the data into bins. Returns the binned data and the bin centers.

    hist = Array on length eual to number of beans. Each element is the number of data points in that bin.
    bin_centers = Array of length equal to number of bins. Contains the value of the bin 
    
    """

    
    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])

    # Plot the binned data
    plt.figure(figsize=(9,6))
    plt.title('Dihedral Angles for rc 10 from Binned data \n',fontsize=16,fontweight='bold')
    plt.bar(bin_centers, hist, width=0.1)
    plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
    plt.ylabel('Frequency',fontsize=14)
    plt.show()
    
    return hist, bin_centers

# # Test the function with the bins going from -pi to pi unsing 100 bins
# hist, bin_centers = bin_data(dih_rc_10[:,1], bins=100)

# Define a function to normalize and plot normalized data 

def normalized_data(data, bins, title):
    """
    Normalize and Plot the normalized histogram of the data.
    """
    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    hist_norm = hist / float(len(data))

    plt.figure(figsize=(9,6))
    plt.title(title,fontsize=16,fontweight='bold')
    plt.bar(bin_centers, hist_norm, width=0.1)
    plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
    plt.ylabel('Frequency',fontsize=14)
    plt.show()

    #Try except block to catch the error if the data is not normalized
    try:
        assert np.allclose(hist_norm.sum(), 1.0)

    except AssertionError:
        print('Data is not normalized')

# # Test the function with the bins going from -pi to pi unsing 100 bins
# normalized_data(dih_rc_10[:,1], bins=100, title='Dihedral Angles for rc 10 from Normalized Binned data \n')



# Define a function to normalize and plot normalized data 

def normalized_data(data, bins, title):
    """
    Normalize and Plot the normalized histogram of the data.
    """
    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    hist_norm = hist / float(len(data))

    plt.figure(figsize=(9,6))
    plt.title(title,fontsize=16,fontweight='bold')
    plt.bar(bin_centers, hist_norm, width=0.1)
    plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
    plt.ylabel('Frequency',fontsize=14)
    plt.show()

    #Try except block to catch the error if the data is not normalized
    try:
        assert np.allclose(hist_norm.sum(), 1.0)

    except AssertionError:
        print('Data is not normalized')

## Test the function with the bins going from -pi to pi unsing 100 bins
#normalized_data(dih_rc_10[:,1], bins=100, title='Dihedral Angles for rc 10 from Normalized Binned data \n')


# Define a function to calculate and plo the free energy of the dihedral angles

def free_energy(data, bins, title):
    """
    Calculate and plot the free energy of the dihedral angles.
    """
    # Denfine boltzmann constant in kj/mol
    k_b = 0.0083144621

    T = 600 # Kelvin

    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_width = np.pi - (-np.pi)
    pdf = hist / sum(hist) / bin_width

    free_energy = -k_b * T * np.log(pdf)

    # Bring back to reference state by subtracting the minimum free energy to all values
    free_energy -= np.min(free_energy)

    plt.figure(figsize=(9,6))
    plt.title(title,fontsize=16,fontweight='bold')
    plt.plot(bin_centers, free_energy)
    plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
    plt.ylabel('Free Energy (KJ/mol) ',fontsize=14)
    plt.show()

## Test the function with the bins going from -pi to pi unsing 100 bins
#free_energy(dih_rc_10[:,1], bins=50, title='Free Energy of Dihedral Angles for rc 10 from PDF \n')


# Put iall in the same plot 
def dihedral_angle_analysis(data, bins, title, plot_type='hist'):
    """
    Analyze the dihedral angles data and plot the selected plot type.
    Available plot types: hist, normalized, pdf, free_energy

    data: numpy array containing the dihedral angles data
    bins: number of bins to use in the histogram
    title: title for the plot
    plot_type: type of plot to generate (hist, normalized, pdf, free_energy)
    """
    k_b = 0.0083144621
    T = 600 # Kelvin

    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    bin_width = np.pi - (-np.pi)

    if plot_type == 'hist':
        plt.figure(figsize=(9,6))
        plt.title(title,fontsize=16,fontweight='bold')
        plt.bar(bin_centers, hist, width=0.1)
        plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
        plt.ylabel('Frequency',fontsize=14)
        plt.show()
        
    elif plot_type == 'normalized':
        hist_norm = hist / float(len(data))

        plt.figure(figsize=(9,6))
        plt.title(title,fontsize=16,fontweight='bold')
        plt.bar(bin_centers, hist_norm, width=0.1)
        plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
        plt.ylabel('Frequency',fontsize=14)
        plt.show()

        try:
            assert np.allclose(hist_norm.sum(), 1.0)

        except AssertionError:
            print('Data is not normalized')
            
    elif plot_type == 'pdf':
        pdf = hist / sum(hist) / bin_width

        plt.figure(figsize=(9,6))
        plt.title(title,fontsize=16,fontweight='bold')
        plt.plot(bin_centers, pdf)
        plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
        plt.ylabel('Probablitity density ',fontsize=14)
        plt.show()
        
    elif plot_type == 'free_energy':
        pdf = hist / sum(hist) / bin_width
        free_energy = -k_b * T * np.log(pdf)
        free_energy -= np.min(free_energy)

        plt.figure(figsize=(9,6))
        plt.title(title,fontsize=16,fontweight='bold')
        plt.plot(bin_centers, free_energy)
        plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
        plt.ylabel('Free Energy (KJ/mol) ',fontsize=14)
        plt.show()

    elif plot_type == 'all':
        hist_norm = hist / float(len(data))
        pdf = hist / sum(hist) / bin_width
        free_energy = -k_b * T * np.log(pdf)
        free_energy -= np.min(free_energy)

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,6))
        fig.suptitle(title,fontsize=16,fontweight='bold')

        ax1.bar(bin_centers, hist, width=0.1)
        ax1.set_xlabel('Dihedral Angle (degrees)',fontsize=14)
        ax1.set_ylabel('Frequency',fontsize=14)

        ax2.plot(bin_centers, pdf)
        ax2.set_xlabel('Dihedral Angle (degrees)',fontsize=14)
        ax2.set_ylabel('Probablitity density ',fontsize=14)

        ax3.plot(bin_centers, free_energy)
        ax3.set_xlabel('Dihedral Angle (degrees)',fontsize=14)
        ax3.set_ylabel('Free Energy (KJ/mol) ',fontsize=14)

        plt.show()

## Test the function with the bins going from -pi to pi unsing 100 bins
#dihedral_angle_analysis(dih_rc_10[:,1], bins=50, title='Free Energy of Dihedral Analysis for rc 10 from PDF \n', plot_type='all')

def free_energy_smooth(data, bins, title):
    """
    Calculate and plot the free energy of the dihedral angles.
    """
    # Denfine boltzmann constant in kj/mol
    k_b = 0.0083144621

    T = 600 # Kelvin

    bin_width = np.pi - (-np.pi)
    hist, bin_edges = np.histogram(data, bins=bins)
    bin_centers = 0.5 * (bin_edges[1:] + bin_edges[:-1])
    hist_smooth = hist / sum(hist) / bin_width

    pdf = gaussian_filter1d(hist_smooth, sigma=1)

    free_energy = -k_b * T * np.log(pdf)

    # Bring back to reference state by subtracting the minimum free energy to all values
    free_energy -= np.min(free_energy)

    # Smooth the free energy curve
    free_energy_smooth = gaussian_filter1d(free_energy, sigma=1)

    plt.figure(figsize=(9,6))
    plt.title(title,fontsize=16,fontweight='bold')
    plt.plot(bin_centers, free_energy_smooth)
    plt.xlabel('Dihedral Angle (degrees)',fontsize=14)
    plt.ylabel('Free Energy (KJ/mol) ',fontsize=14)
    plt.show()