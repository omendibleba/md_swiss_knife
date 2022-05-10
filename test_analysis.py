import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import os


# Number of the model testing
mod_num = "5"


#Create files to store testing plots 
path = os.getcwd()
try:
    os.mkdir(path+"/test_analysis")
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)


# Load the learning curve rate
lcrv_txt = 'x'
lcurve = (lcrv_txt)


#PLot the total Mean Squared Error 
plt.figure(figsize=(12,9),facecolor='white')
plt.yscale('log')
plt.plot(lcurve[:,1], label ='Total MSE ', color = 'red')
plt.xlabel('Step', fontsize =16)
plt.ylabel("",fontsize =16)
plt.xticks(fontsize =16)
plt.yticks(fontsize =16)
plt.legend(fontsize =16)
plt.savefig('totalMSE_'+mod_num+'k.png')


# Plot the Learning curve
plt.figure(figsize=(12,9),facecolor='white')
#plt.yscale('log')
plt.plot(lcurve[:,7], label ='Learning Rate')
plt.xlabel('Step', fontsize =16)
plt.ylabel("",fontsize =16)
plt.xticks(fontsize =16)
plt.yticks(fontsize =16)
plt.legend(fontsize =16)
plt.savefig('LearningR_'+mod_num+'k.png')


# Load the output files form testing the model.## Remember to change the name of the files 
test_e = np.loadtxt('test_2k/test_300.e.out')
test_f = np.loadtxt('test_2k/test_300.f.out')


# DEtermine the R2 for the energy
r2_model = r2_score(test_e[:,1],test_e[:,0])
r2_model = round(r2_model,4)
r2_model


# Plot the prediction energy vs the actual(test) energy 
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(test_e[:,0],test_e[:,1],color='b')
plt.plot([-30006,-30003],[-30006,-30003], color='r')
plt.plot([],[],label='$R^2$ = {} %'.format(r2_model))
plt.title(mod_num+"K_Model Total Energy Prediction Test",fontsize=18,fontweight = 'bold')
plt.xlabel("Test Energy (eV)",fontsize=16)
plt.ylabel("Predicted Energy (eV)",fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize =16)
plt.savefig('TotEng_Testing_'+mod_num+'K_.png')


print("Script Sucessfully Created Plots")