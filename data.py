# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

#PATH = r'C:\Users\442491\Documents\Lots Dashboard'
PATH = r'/Users/isabellehirschy/Documents/Lot Dashboard'

df = pd.read_csv(os.path.join(PATH, 'list_of_properties.csv'))

# Make Socrata API Call

# Clean data

def make_date(col, df, split=False):
    if split == True:
        df[["Month Sold", "Day Sold", "Year Sold"]] = df[col].str.split("/", expand=True)
        df["Date_Sold"] = df["Month Sold"] + "-" + df["Year Sold"]
        df["Date_Sold"] = pd.to_datetime(df["Date_Sold"], infer_datetime_format=True, errors='coerce')
        df.drop(["Month Sold", "Day Sold", "Year Sold"], axis=1)
    else:
        df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors='coerce')
    return df

df = make_date('Date Property  Was Sold', df, split=True)

# Split into the grouped data we want

df_sold = df[df["Owership Status"] == "Sold"]

df_sold_grouped = df_sold.groupby('Date_Sold')['Address'].count()

df_sold_grouped = df_sold_grouped.reset_index()

df_sold_grouped = df_sold_grouped[df_sold_grouped["Date_Sold"] >= '2020-01-01']

df_ais_grouped = df.groupby("AIS Category")["Address"].count()
df_ais_grouped = df_ais_grouped.reset_index()
df_ais_grouped = df_ais_grouped.rename(columns={"AIS Category":"AIS_Category"})

# Export to CSVs

df_sold_grouped.to_csv(os.path.join(PATH, "lots_sold.csv"), index=False)
df_ais_grouped.to_csv(os.path.join(PATH, "ais_review.csv"), index=False)

# Number of Lots Sold Per Month
#p = sns.barplot(df_sold_grouped["Date Sold"], df_sold_grouped["Address"])
#p.set(xticklabels = [])



'''
df = make_date('Date Property Was Added', df)
df = make_date('Date Property Was Purchased', df)
df = make_date('Date Property  Was Sold', df, split=True)
df - make_date('Date of  Last Update', df)
'''