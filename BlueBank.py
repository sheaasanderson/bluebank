#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 12 12:26:05 2023

"""

import json
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# Reading json data
with open('loan_data_json.json') as json_file:
    data = json.load(json_file)
  

# Transform json to data frame
loandata = pd.DataFrame(data)


# Finding unique values in 'purpose' column
loandata['purpose'].unique()


# Describing data (and for specific columns)
loandata.describe()
loandata['int.rate'].describe()
loandata['fico'].describe()
loandata['dti'].describe()


# Using exp() to get annual income from log.annual.inc
loandata['annualincome'] = np.exp(loandata['log.annual.inc'])


# Applying 'for loops' to FICO score
length = len(loandata)
ficocat = []
for x in range(0,length):
    category = loandata['fico'][x]
    if category >= 300 and category < 401:
        cat = 'Very Poor'
    elif category >= 401 and category < 601:
        cat = 'Poor'
    elif category >= 601 and category < 661:
        cat = 'Fair'
    elif category >= 661 and category < 781:
        cat = 'Good'
    elif category >= 781:
        cat = 'Excellent'
    else:
        cat = 'Unknown'
    ficocat.append(cat)
    
ficocat = pd.Series(ficocat)
loandata['fico.category'] = ficocat


# For interest rates, a new column is wanted (rate > 0.12 then high, else low)
loandata.loc[loandata['int.rate'] > 0.12, 'int.rate.type'] = 'High'
loandata.loc[loandata['int.rate'] <= 0.12, 'int.rate.type'] = 'Low'


# Plotting number of loans by fico category
catplot = loandata.groupby(['fico.category']).size() # 'size' is the number of rows

catplot.plot.bar(color = 'green', width = 0.1)
plt.show()


# Scatter plot of dti compared to annual income
ypoint = loandata['annualincome']
xpoint = loandata['dti']
plt.scatter(xpoint, ypoint, color = '#4CAF50')
plt.show()


# Writing to csv
loandata.to_csv('loan_cleaned.csv', index = True) # since there's no unique ID per applicant, we need to keep the index


