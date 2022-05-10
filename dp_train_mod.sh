#!/bin/sh

# This scripth is able to generate the training data and submit the
#MOdel for training. 

# Cretate output folder and copy trajecotry and log file 
mkdir output
mv DP2_330_2K-pos-1.xyz dptry2_330_2K.log output/


# Create training data with dp data 
python3 dp_data_create.py


#Create folder for valaidation data and mv random sets to this folder. 
mkdir validation
cd training
shuf -n 400 -e * | xargs -i mv {} ../validation

# Make sure both raw files are on both folders 
cp *.raw ../validation
cp ../validation/*.raw .
cd ..

# Copy the testing data 
mkdir test_2k
cp -R ~/dptry2/330_5K/depmd5k/test_5k/test_data_2kT test_2k/
echo Testing data copied successfully

# Submit the model for training.## REMEMBER TO CAHNGE THE NAME OF THE SUBMISSION FILE  
qsub sub_train_exp.sh

echo Model submmited for training successfully


