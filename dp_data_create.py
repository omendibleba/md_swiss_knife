import dpdata 
import numpy as np


# Lets read the output and trajectory of the 300_2K run 
output_330_2k = dpdata.LabeledSystem('330_2K/output', fmt="cp2k/aimd_output")
print(output_330_2k)


# create folders
output_330_2k.to_deepmd_npy('330_2K/training', set_size = 1, prec = np.float32)
print('Training folder created successfully')


