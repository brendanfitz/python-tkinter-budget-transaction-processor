# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 13:58:46 2020

@author: Brendan Non-Admin

an analysis of my banking transactions to determine the maximum column character limit

"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open('../data/filepath.txt', 'r') as f:
    filepath = f.read()
    
sheet_names = ['Checking', 'Credit Card']
sheet_name = sheet_names[0]

frames = []
for sheet_name in sheet_names:
    df = pd.read_excel(filepath, sheet_name).loc[:, ['Description']]
    frames.append(df)

df = pd.concat(frames, axis=0)

max_description = df.Description.str.len().max()
print(f"Maximum Description character Length: {max_description:5.0f}")

sns.distplot(df.Description.str.len(), kde=False)

"""
We'll choose 65 since it is slightly larger than 2nd order mode
"""