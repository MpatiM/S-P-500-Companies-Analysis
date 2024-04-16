# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 16:10:56 2023

@author: Kanna
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stat

## ACTIVITY DATA

path = "C:/Users/Kanna/Documents/Rutgers Grad/Spring 2023/BINF5900 DATA SCIENCE PROG/Final_Project_Data/"

## LOAD ALL DATASETS
# Daily Calories
dc = pd.read_csv(path+"dailyCalories.csv", na_filter = True)
print("Daily Calories:\n", dc)

print(dc.columns)
    # Index(['Id', 'ActivityDay', 'Calories'], dtype='object')
    
# Daily Steps
ds = pd.read_csv(path+"dailySteps.csv", na_filter = True)
print("Daily Steps:\n", ds)

print(ds.columns)
    # Index(['Id', 'ActivityDay', 'StepTotal'], dtype='object')
    
# Daily Intensities
di = pd.read_csv(path+"dailyIntensities.csv", na_filter = True)
print("Daily Intensities:\n", di)

print(di.columns)
    # Index(['Id', 'ActivityDay', 'SedentaryMinutes', 'LightlyActiveMinutes',
    #        'FairlyActiveMinutes', 'VeryActiveMinutes', 'LightActiveDistance',
    #        'ModeratelyActiveDistance', 'VeryActiveDistance'],
    #       dtype='object')

# Daily Sleep
sleep = pd.read_csv(path+"sleepDay.csv", na_filter = True)
print("Daily Sleep:\n", ds)

print(ds.columns)
    # Index(['Id', 'ActivityDay', 'StepTotal'], dtype='object')
    
## CLEAN AND VALIDATE THE DATASETS

# Clean Dataset Daily Calories
dc.columns

# Verify for Duplicates
dc[['Id', 'ActivityDay']].count()  # Display total number

dc[['Id', 'ActivityDay']].nunique()  # Display total unique values  

dc[['Id', 'ActivityDay']].duplicated().any()   # Displays booleon of duplicate value as True
    # Observed False as there are no duplicates
    # NO DUPLICATES
    
# Clean Dataset Daily Steps
ds.columns

# Verify for Duplicates
ds[['Id', 'ActivityDay']].count()  # Display total number

ds[['Id', 'ActivityDay']].nunique()  # Display total unique values  

ds[['Id', 'ActivityDay']].duplicated().any()   # Displays booleon of duplicate value as True
    # Observed False as there are no duplicates
    # NO DUPLICATES
    
# Clean Dataset Daily Intensity

# Verify for Duplicates
di.columns

di[['Id', 'ActivityDay']].count()  # Display total number

di[['Id', 'ActivityDay']].nunique()  # Display total unique values  

di[['Id', 'ActivityDay']].duplicated().any()   # Displays booleon of duplicate value as True
    # Observed False as there are no duplicates
    # NO DUPLICATES

# Clean Dataset Daily Sleep

# Verify for Duplicates
sleep.columns

sleep[['Id', 'SleepDay']].count()  # Display total number

sleep[['Id', 'SleepDay']].nunique()  # Display total unique values  

sleep[['Id', 'SleepDay']].duplicated().any()   # Displays booleon of duplicate value as True
    # Observed True
    # THERE ARE DUPLICATES
    
# Get rid of Duplicates
sleep.drop_duplicates(subset = ['Id', 'SleepDay'], inplace=True)

# Verify if Dropped
sleep[['Id', 'SleepDay']].duplicated().any()
    # Observed False as there are no more duplicates
    
# Rename column SleepDay to ActivityDay in Daily Sleep 
sleep.rename(columns = {'SleepDay':'ActivityDay'}, inplace=True)
sleep.columns   # Verify

# Convert all AcitivityDay to pandas datetime
dc['ActivityDay'] = pd.to_datetime(dc['ActivityDay'])
dc['ActivityDay']   # Verify

ds['ActivityDay'] = pd.to_datetime(ds['ActivityDay'])
ds['ActivityDay']   # Verify

di['ActivityDay'] = pd.to_datetime(di['ActivityDay'])
di['ActivityDay']   # Verify

sleep['ActivityDay'] = pd.to_datetime(sleep['ActivityDay'])
sleep['ActivityDay']   # Verify; confirm there is no time

# SAVE DATAFRAMES
dc.to_pickle(path+'dcal.pkl')
ds.to_pickle(path+'dstep.pkl')
di.to_pickle(path+'dinten.pkl')
sleep.to_pickle(path+'dsleep.pkl')

# LOAD DATAFRAMES
dc = pd.read_pickle(path+'dcal.pkl')
ds = pd.read_pickle(path+'dstep.pkl')
di = pd.read_pickle(path+'dinten.pkl')
sleep = pd.read_pickle(path+'dsleep.pkl')

## MERGE DATASETS
# Merged data frame is da_merged (Daily Activity)
da_merged = pd.merge(dc, ds, how="left", on=['Id', 'ActivityDay'])
da_merged = pd.merge(da_merged, di, how='left', on=['Id', 'ActivityDay'])
da_merged = pd.merge(da_merged, sleep, how='left', on=['Id', 'ActivityDay'])

print("Merged Datasets:\n", da_merged)

print("Columns of Merged Data:\n", da_merged.columns)


# Set columns 'Id' and 'ActivityDay' as index for new dataframe 'da'
da = da_merged.set_index(['Id', 'ActivityDay'])
print("Daily Activity:\n", da)

print("Columns of Merged Data Daily Activity:\n", da.columns)

# add to da summary columns total active minutes and total active distance
mapping = {'LightlyActiveMinutes':'TotalActiveMinutes',
           'FairlyActiveMinutes':'TotalActiveMinutes',
           'VeryActiveMinutes':'TotalActiveMinutes',
           'LightActiveDistance':'TotalActiveDistance',
           'ModeratelyActiveDistance':'TotalActiveDistance',
           'VeryActiveDistance':'TotalActiveDistance'}

by_column = da.groupby(mapping, axis=1)
by_column.sum()

da[['TotalActiveDistance', 'TotalActiveMinutes']] = by_column.sum()
    # Add two new columns that summarize active minutes and active distance

# SAVE MERGED DATASET
da.to_pickle(path+'dactiv.pkl')
# LOAD DATASET
da = pd.read_pickle(path+'dactiv.pkl')


## REPORTS
da.columns

## Report 1
# List daily summary data with Total Calories, Total Steps, Total Active Minutes, 
# Total Active Distance, Total Minutes Asleep 
report_1 = da[['Calories', 'StepTotal', 'TotalActiveDistance', 
               'TotalActiveMinutes', 'TotalMinutesAsleep']]

## Report 2
# List average Calories, StepTotal, all columns with minuts, 
# all columns with distance by Id
report_2 = da.groupby(['Id'])[['Calories', 'StepTotal', 'SedentaryMinutes', 'LightlyActiveMinutes',
                               'FairlyActiveMinutes', 'VeryActiveMinutes', 'LightActiveDistance',
                               'ModeratelyActiveDistance', 'VeryActiveDistance']].mean()

## Report 3
# Statistics for data by Id with Total Calories, Total Steps, Total Active Minutes, 
# Total Active Distance, Total Minutes Asleep 
report_3 = da.groupby(['Id'])[['Calories', 'StepTotal', 'TotalActiveDistance', 
                               'TotalActiveMinutes', 'TotalMinutesAsleep']].describe()

## Report 4
# List for each Id, correlation between Total Steps and Calories
overall_corr = da['StepTotal'].corr(da['Calories'])

##_______________________________________________________

corr_df = da.groupby(['Id'])[['StepTotal', 'Calories']].sum()

corr_df['Correlation'] = da.groupby(['Id'])['StepTotal'].corr(da['Calories'])

# Display Bar Graph between Id and Correlation
# corr_data = corr_df['Correlation']

# plt.figure(figsize=(8,8))
# plt.title("Correlation between StepTotal and Calories by Id's")
# corr_data.plot.bar()
# plt.xlabel('ID')
# plt.ylabel('Correlation')
# plt.grid(axis='y', color='r', linestyle='--')
# plt.show()

# # Display Line Graph of StepTotal vs. Calories for entire data
# sorted_corr_df = corr_df.sort_values(by='StepTotal')

# sorted_corr_df.plot.line('StepTotal', 'Calories')
# plt.title("StepTotal vs. Calories")
# plt.xlabel('StepTotal')
# plt.ylabel('Calories')
# plt.grid(axis='y', color='k', linestyle='--')
# plt.show()

################# USE THIS ####################
# Subplot of both graphs using Sorted Corr Data
sorted_corr_df = corr_df.sort_values(by='StepTotal')

fig, axis = plt.subplots(2, 1, figsize=(10,8))

sorted_corr_df.plot.line('StepTotal', 'Calories', ax = axis[0], color = 'r')
axis[0].set_title("StepTotal vs. Calories")
axis[0].set_xlabel('StepTotal')
axis[0].set_ylabel('Calories')
axis[0].grid(axis='y', color='k', linestyle='--')

corr_data = sorted_corr_df['Correlation']
corr_data.plot.bar(ax = axis[1], color='b')
axis[1].set_title("Correlation between StepTotal and Calories by Id's")
axis[1].set_xlabel('ID')
axis[1].set_ylabel('Correlation')
axis[1].grid(axis='y', color='k', linestyle='--')

plt.tight_layout()
plt.show()

## Report 5
# linear regression to show how calories is affected by totalactivedistance and totalactiveminutes
import statsmodels.api as ss

x = da['Calories']
y = da['TotalActiveDistance']
z = da['TotalActiveMinutes']

model = ss.OLS(x, y+z).fit()
prediction = model.predict(x)
prediction

model.summary()  
    # R2 = 88.3% variation on calories
    # coef = 1.8097 means changing the ind. values by this much will increase calories
    # there is only a std err of 0.022 between actual and predicted values
    # Can look into p-value - it is less than 0.05 which means we reject the hypothesis that calories will increase when increasing ind vars
        # CAN ALSO MEAN the value is statistically significant

################################ EXPLANATION ##################################

# P values and coefficients in regression analysis work together to tell you 
# which relationships in your model are statistically significant and the nature of those relationships. 
# The linear regression coefficients describe the mathematical relationship between 
# each independent variable and the dependent variable. 
# The p values for the coefficients indicate whether these relationships are statistically significant.

# After fitting a regression model, check the residual plots first to be sure 
# that you have unbiased estimates. After that, it’s time to interpret the statistical output. 
# Linear regression analysis can produce a lot of results, which I’ll help you navigate. 
# In this post, I cover interpreting the linear regression p-values and coefficients 
# for the independent variables.

# Regression analysis is a form of inferential statistics. 
# The p values in regression help determine whether the relationships that you 
# observe in your sample also exist in the larger population. The linear regression 
# p value for each independent variable tests the null hypothesis that the variable 
# has no correlation with the dependent variable. If there is no correlation, 
# there is no association between the changes in the independent variable and the 
# shifts in the dependent variable. In other words, there is insufficient evidence 
# to conclude that there is an effect at the population level.

# If the p-value for a variable is less than your significance level, your 
# sample data provide enough evidence to reject the null hypothesis for the entire 
# population. Your data favor the hypothesis that there is a non-zero correlation. 
# Changes in the independent variable are associated with changes in the dependent 
# variable at the population level. This variable is statistically significant 
# and probably a worthwhile addition to your regression model.

# The sign of a linear regression coefficient tells you whether there is a 
# positive or negative correlation between each independent variable and the 
# dependent variable. A positive coefficient indicates that as the value of the 
# independent variable increases, the mean of the dependent variable also tends 
# to increase. A negative coefficient suggests that as the independent variable 
# increases, the dependent variable tends to decrease.

# The coefficient value signifies how much the mean of the dependent variable 
# changes given a one-unit shift in the independent variable while holding other 
# variables in the model constant.

###############################################################################

# Plotting linear regression
plt.figure(figsize=(8,8))

plt.title("Linear Regression on Calories")
plt.xlabel("Calories")
plt.ylabel("Prediction")

plt.scatter(x, prediction, c='b', marker='o')

m, b = np.polyfit(x, prediction, 1)
plt.plot(x, m*x + b, c='k')

plt.show()


da['Calories'], prediction

###############################################
# Using scipy stats
###############################################

## Normality of the data
# H0: 'StepTotal' distribution is the same as normal distribution
# H1: 'StepTotal' distribution is not the same as normal distribution

norm_report = stat.normaltest(da['StepTotal'])

    # The p-value is equal to 2.4709, indicating we accept the null hypothesis
    
## Report 6 - run a one-way anova test
# H0: The mean of totalsteps is equal to 10,000
# H1: The mean of totalsteps is not equal to 10,000
    # P value is < 0.05 (Accepting Alternative Hypothesis)

report_6 = stat.ttest_1samp(da['StepTotal'], 10000)

    # the p-value is equal to 8.739, indicating we accept the null hypothesis,
    # where the mean value of StepTotal is equal to 10,000
