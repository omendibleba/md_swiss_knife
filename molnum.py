#script to ask user for box size, density, molar mass to determine how many molecules 
# required for a simulation box of desired density


# Ask user for desired density and molar mass of nolecule of interest 

dens = float(input('Insert density of simulation box(g/cm_^3): '))
mm = float(input("Insert Molar mass of molecule of interest: (g/mol): "))
lx = float(input('Insert length of x-axis(Armstrong): '))
ly = float(input('Insert length of y-axis(Armstrong): '))
lz = float(input('Insert length of z-axis(Armstrong): '))


# Determine volume of the simulation box and change to m 
vol_a = lx*ly*lz ##A^3

## 1 A = 10^-7 m
arm = 10**(-10) #m 
vol_m = vol_a* arm**3 ##m^3


# Use inputs to determine molarity (mol/cm3) 

molarity_cm = dens/mm # mol/cm3
molarity_m = molarity_cm*(100**3)  #mol/m3

# Define avogadro's number
Na = 6.022*(10**23) ## particle/mol


# Determine the number of molecules and print results

num = molarity_m*vol_m*Na

print('Box size: ', vol_a,'Armstrong^3')
print('Density of :', dens, 'g/cm3')
print('The required number of molecules is: ',round(num))