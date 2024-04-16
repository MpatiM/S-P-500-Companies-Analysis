# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 21:19:16 2023

@author: Kanna
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

## DISEASE SYMPTOMS, PRECAUTION, RISK FACTORS

path = "C:/Users/Kanna/Documents/Rutgers Grad/Spring 2023/BINF5900 DATA SCIENCE PROG/AdvPy_Project_Final/"

## Load all four datasets
# Disease Symptoms
ds = pd.read_csv(path+"disease_symptoms.csv", na_filter = True)
print("Disease Symptoms:\n", ds)

print(ds.columns)

# Disease Medicine   # Saved as CSV UTF-8 file
dm = pd.read_csv(path+"disease_medicine.csv", na_filter = True)
print("Disease Medicine:\n", dm)

print(dm.columns)

# Disease Precaution
dp = pd.read_csv(path+"disease_precaution.csv", na_filter = True)
print("Disease Precaution:\n", dp)

print(dp.columns)

# Disease RiskFactors   # Saved as CSV UTF-8 file
dr = pd.read_csv(path+"disease_riskFactors.csv", na_filter = True)
print("Disease Risk Factors:\n", dr)

print(dr.columns)

## Clean and Validate the datasets

# print(dr.columns)
# Index(['DID', 'DNAME', 'PRECAU', 'OCCUR', 'RISKFAC'], dtype='object')


## Clean data in Disease Symptoms
# print(ds.columns)
# Index(['Disease', 'Symptom_1', 'Symptom_2', 'Symptom_3', 'Symptom_4',
#        'Symptom_5', 'Symptom_6', 'Symptom_7', 'Symptom_8', 'Symptom_9',
#        'Symptom_10', 'Symptom_11', 'Symptom_12', 'Symptom_13', 'Symptom_14',
#        'Symptom_15', 'Symptom_16', 'Symptom_17'],
#       dtype='object')

# Duplicates
ds['Disease'].count()  # Display total number in Disease

ds['Disease'].nunique()  # Display total unique values in Disease 

ds['Disease'].duplicated()   # Displays booleon of duplicate value as True

    # NO DUPLICATES

# Make Title Case if not all Upper Case
########## WORK NOTES ##########
'AIDS'.isupper()
'Aids'.isupper()
################################
col_mask = (ds['Disease'].str.isupper())
col_mask

ds['Disease'][col_mask]   # list columns that are NOT all uppercase

# Replace the values that are identiied as boolean False in col_mask with title case value
ds['Disease'][~col_mask] = ds['Disease'][~col_mask].str.title()

ds['Disease']

# Clean data to make sure there is no white-spaces before values
ds['Symptom_1'][5]  # for verification

for i in ds.columns:
    ds[i] = ds[i].str.lstrip()

ds['Symptom_1'][5]   # verify 

# Save Data
ds.to_pickle(path+'ds.pkl')
ds = pd.read_pickle(path+'ds.pkl')

## Clean data in Disease Medicines
# print(dm.columns)
# Index(['Medicine_ID', 'Medicine_Name', 'Disease_ID', 'Medicine_Composition',
#        'Medicine_Description'],
#       dtype='object')

# Clean data to make sure there are no white-space characters before/after values
for i in dm.columns:
    if dm[i].dtype == 'object':
        # print(i)
        dm[i] = dm[i].str.strip()
    else:
        pass

dm

# Make Medicine Name title case
row = 0

for name in dm['Medicine_Name'].astype('str'):
    if name[0].islower():
        print(name)
        name1 = name[0].upper() + name[1:]
        print(name1)
        dm.at[row, 'Medicine_Name'] = name1
    else:
        # do nothing
        pass
    
    row += 1
    
dm['Medicine_Name'][4]   # validation to check if first letter converted to uppercase
dm['Medicine_Name'][15]   # validation to check if it remains the same
  
dm['Medicine_Name']

# Duplicates
dm[['Medicine_ID', 'Medicine_Name']].count()   # Display total in Medicine_ID
dm[['Medicine_ID', 'Medicine_Name']].nunique()   # Display total unique in Medicine_ID
dm[['Medicine_ID', 'Medicine_Name']].duplicated().any()   # Displays booleon of duplicate value as True

    # THERE ARE DUPLICATES

# Get rid of duplicates
dm.drop_duplicates(subset = ['Medicine_ID', 'Medicine_Name'], inplace=True)

dm[['Medicine_ID', 'Medicine_Name']].count()   # verify
dm[['Medicine_ID', 'Medicine_Name']].nunique()   # verify
dm[['Medicine_ID', 'Medicine_Name']].duplicated().any()   # verify

dm['Medicine_Name'].duplicated()

dm

# Save Data
dm.to_pickle(path+'dm.pkl')
dm = pd.read_pickle(path+'dm.pkl')

## Clean data in Disease Precautions
# print(dp.columns)
# Index(['Disease', 'Precaution_1', 'Precaution_2', 'Precaution_3',
#        'Precaution_4'],
#       dtype='object')

