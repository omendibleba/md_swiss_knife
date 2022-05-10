import lammps_logfile
import matplotlib.pyplot as plt
import numpy as np


log_file_name = "dmf_18_NPT.log"

log = lammps_logfile.File(log_file_name)

step = log.get("Step")
temp = log.get("Temp")

# Temperature average
temp_ave = round(np.average(temp),2)

# PLot temp 
plt.plot(step,temp,color="blue")
plt.hlines(temp_ave,xmin=min(step),xmax=max(step),color="red",label = "Average Pressure = {} K".format(temp_ave))
plt.xlabel("Step")
plt.ylabel("Temperature (K)")
plt.legend()
plt.show()


# Pressure 
press = log.get("Press")
press_ave = round(np.average(press),3)
plt.plot(step,press,color="blue")
plt.hlines(press_ave,xmin=min(step),xmax=max(step),color="red",label = "Average Pressure = {} atm".format(press_ave))
plt.xlabel("Step")
plt.ylabel("Pressure (atm)")
plt.legend()
plt.show()

#Volume
vol = log.get("Volume")
vol_ave = round(np.average(vol),3)
vol_ave_40K = round(np.average(vol[50000::]),3)
plt.plot(step,vol,color="blue")
plt.hlines(vol_ave,xmin=min(step),xmax=max(step),color="black",label = "Average Volume = {} $A^3$ ?".format(vol_ave))
plt.hlines(vol_ave_40K,xmin=50000,xmax=max(step),color="red",label = "Average Volume After 50K steps = {} $A^3$ ?".format(vol_ave_40K))
plt.title('Volume')
plt.xlabel("Step")
plt.ylabel("Volume ($A^3$)")
plt.legend()
plt.show()


#Density 
dens = log.get("Density")
dens_ave = round(np.average(dens),2)
plt.plot(step,dens,color="blue")
plt.hlines(dens_ave,xmin=min(step),xmax=max(step),color="red",label = "Average Density = {} g/$cm^3$ ".format(dens_ave))
plt.title("Density")
plt.xlabel("Step")
plt.ylabel("Density (g/$cm^3$)")
plt.legend()
plt.show()


# Total Energy 
totEng = log.get("TotEng")
totEng_ave = round(np.average(totEng),2)
plt.plot(step,totEng,color="blue")
plt.hlines(totEng_ave,xmin=min(step),xmax=max(step),color="red",label = "Average Total Energy = {} Kcal/mol ".format(totEng_ave))
plt.title("Total Energy ")
plt.xlabel("Step")
plt.ylabel("Total Energy (Kcal/mol)")
plt.legend()
plt.show()


#Potential Energy 
potEng = log.get("PotEng")
potEng_ave = round(np.average(potEng),2)
plt.plot(step,potEng,color="blue")
plt.hlines(potEng_ave,xmin=min(step),xmax=max(step),color="red",label = "Average Potential Energy = {} Kcal/mol ".format(potEng_ave))
plt.title("Potential Energy ")
plt.xlabel("Step")
plt.ylabel("Potential Energy (Kcal/mol)")
plt.legend()
plt.show()


# Kinetic Energy 
kinEng = log.get("KinEng")
kinEng_ave = round(np.average(kinEng),2)
plt.plot(step,kinEng,color="blue")
plt.hlines(kinEng_ave,xmin=min(step),xmax=max(step),color="red",label = "Average Kinetic Energy = {} Kcal/mol ".format(kinEng_ave))
plt.title("Kinetic Energy ")
plt.xlabel("Step")
plt.ylabel("Kinetic Energy (Kcal/mol)")
plt.legend()
plt.show()
