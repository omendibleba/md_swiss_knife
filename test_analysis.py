import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import os


# Number of the model testing
mod_name = "name_model"


#Create files to store testing plots 
path = os.getcwd()
try:
    os.mkdir(path+"/test_analysis")
except OSError:
    print ("Creation of the directory %s failed" % path)
else:
    print ("Successfully created the directory %s " % path)


# Load the learning curve rate
lcrv_txt = 'name_of_lcurve_file'
lcurve = np.loadtxt(lcrv_txt)


#PLot the total Mean Squared Error 
plt.figure(figsize=(12,9),facecolor='white')
plt.yscale('log')
plt.plot(lcurve[:,1], label ='Total MSE ', color = 'red')
plt.xlabel('Step', fontsize =16)
plt.ylabel("",fontsize =16)
plt.xticks(fontsize =16)
plt.yticks(fontsize =16)
plt.legend(fontsize =16)
plt.savefig('totalMSE_'+mod_name+'.png')


# Plot the Learning curve
plt.figure(figsize=(12,9),facecolor='white')
#plt.yscale('log')
plt.plot(lcurve[:,7], label ='Learning Rate')
plt.xlabel('Step', fontsize =16)
plt.ylabel("",fontsize =16)
plt.xticks(fontsize =16)
plt.yticks(fontsize =16)
plt.legend(fontsize =16)
plt.savefig('LearningR_'+mod_name+'.png')


# Load the output files form testing the model.## Remember to change the name of the files 
test_e = np.loadtxt('test_10kx01.e.out')
test_f = np.loadtxt('test_10kx01.f.out')


# DEtermine the R2 for the energy
r2_model = r2_score(test_e[:,1],test_e[:,0])
r2_model = round(r2_model,4)
r2_model


# Plot the prediction energy vs the actual(test) energy 
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(test_e[:,0],test_e[:,1],color='b')
plt.plot([min(test_e[:,0]),max(test_e[:,0])],[min(test_e[:,0]),max(test_e[:,0])], color='r')
plt.plot([],[],label='$R^2$ = {} %'.format(r2_model))
plt.title(mod_name+" Model Total Energy Prediction Test",fontsize=18,fontweight = 'bold')
plt.xlabel("Test Energy (eV)",fontsize=16)
plt.ylabel("Predicted Energy (eV)",fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize =16)
plt.savefig('TotEng_Testing_'+mod_name+'_.png')



#Obtain data and prediction in x-axis 
data_fx =test_f[:,0]
pred_fx= test_f[:,3]

# DEtermine the R2 for the force in x-axis 
r2_model = r2_score(data_fx,pred_fx)
r2_model = round(r2_model,4)
r2_model

# Plot the prediction force vs the actual(test) force
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(data_fx,pred_fx,color='b')
plt.plot([min(data_fx),max(data_fx)],[min(data_fx),max(data_fx)], color='r')
plt.plot([],[],label='$R^2$ = {} %'.format(r2_model))
plt.title(mod_name+" Model x-axis Force Prediction Test",fontsize=18,fontweight = 'bold')
plt.xlabel("Test Force (eV/A)",fontsize=16)
plt.ylabel("Predicted Force (eV/A)",fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize =16)
plt.savefig('X-Force_Testing_'+mod_name+'_.png')



#Obtain data and prediction in y-axis 
data_fy =test_f[:,1]
pred_fy= test_f[:,4]

# DEtermine the R2 for the force in x-axis 
r2_model = r2_score(data_fy,pred_fy)
r2_model = round(r2_model,4)
r2_model

# Plot the prediction force vs the actual(test) force
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(data_fy,pred_fy,color='b')
plt.plot([min(data_fy),max(data_fy)],[min(data_fy),max(data_fy)], color='r')
plt.plot([],[],label='$R^2$ = {} %'.format(r2_model))
plt.title(mod_name+" Model y-axis Force Prediction Test",fontsize=18,fontweight = 'bold')
plt.xlabel("Test Force (eV/A)",fontsize=16)
plt.ylabel("Predicted Force (eV/A)",fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize =16)
plt.savefig('Y-Force_Testing_'+mod_name+'_.png')



#Obtain data and prediction in z-axis 
data_fz =test_f[:,2]
pred_fz= test_f[:,5]

# DEtermine the R2 for the force in x-axis 
r2_model = r2_score(data_fz,pred_fz)
r2_model = round(r2_model,4)
r2_model

# Plot the prediction force vs the actual(test) force
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(data_fz,pred_fz,color='b')
plt.plot([min(data_fz),max(data_fz)],[min(data_fz),max(data_fz)], color='r')
plt.plot([],[],label='$R^2$ = {} %'.format(r2_model))
plt.title(mod_name+" Model z-axis Force Prediction Test",fontsize=18,fontweight = 'bold')
plt.xlabel("Test Force (eV/A)",fontsize=16)
plt.ylabel("Predicted Force (eV/A)",fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize =16)
plt.savefig('Z-Force_Testing_'+mod_name+'_.png')




### Add the force data and prediction in all direction to obtain a graph comparing the total forces

data_ftot = np.add(data_fx,data_fy,data_fz)
pred_ftot = np.add(pred_fx,pred_fy,pred_fz)

# Determine r2 for tot force 
# DEtermine the R2 for the force in x-axis 
r2_model = r2_score(data_ftot,pred_ftot)
r2_model = round(r2_model,4)
r2_model

# Plot the prediction force vs the actual(test) force
plt.figure(figsize=(12,9),facecolor='white')
plt.scatter(data_ftot,pred_ftot,color='b')
plt.plot([min(data_ftot),max(data_ftot)],[min(data_ftot),max(data_ftot)], color='r')
plt.plot([],[],label='$R^2$ = {} %'.format(r2_model))
plt.title(mod_name+"Model Force Prediction Test",fontsize=18,fontweight = 'bold')
plt.xlabel("Test Force (eV/A)",fontsize=16)
plt.ylabel("Predicted Force (eV/A)",fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.legend(fontsize =16)
plt.savefig('Total-Force_Testing_'+mod_name+'_.png')

print("Script Sucessfully Created Plots")