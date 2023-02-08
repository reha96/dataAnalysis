#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 31 17:26:35 2023

@author: reha.tuncer
"""

import pandas as pd
import numpy as np
import statsmodels.formula.api as smf
from scipy import stats
from matplotlib import pyplot as plt
from patsy.contrasts import ContrastMatrix
import statsmodels.api as sm
from openpyxl import Workbook
import statsmodels.stats.multicomp as mc
import pingouin as pg


np.random.seed(0)
df = pd.read_excel("dataset.xls", "1")

df.filter(like='NASASUM')  # FILTER by name and get COLUMN
df.filter(like='AGE').astype(str).describe()  # CONVERT to STR and DESCRIBE
df.filter(like='GEN').astype(str).describe()
df.filter(like='EDU').astype(str).describe()
df.filter(like='RAND').astype(str).describe()

df.filter(like='AGE').value_counts() # counts of each value
df.filter(like='GEN').value_counts()
df.filter(like='EDU').value_counts()

y1 = str(df.filter(like='NASASUM').columns[0])
y2 = str(df.filter(like='NASAFRUST').columns[0])
y3 = str(df.filter(like='BENSUM').columns[0])
y4 = str(df.filter(like='UXPRAG').columns[0])
y5 = str(df.filter(like='UXHED').columns[0])
x1 = str(df.filter(like='AGE').columns[0])
x2 = str(df.filter(like='GEN').columns[0])
x3 = str(df.filter(like='EDU').columns[0])
t = str(df.filter(like='RAND').columns[0])

df.rename(columns={y1: 'NASASUM'}, inplace=True)
df.rename(columns={y2: 'NASAFRUST'}, inplace=True)
df.rename(columns={y3: 'BENSUM'}, inplace=True)
df.rename(columns={y4: 'UXPRAG'}, inplace=True)
df.rename(columns={y5: 'UXHED'}, inplace=True)
df.rename(columns={x1: 'AGE'}, inplace=True)
df.rename(columns={x2: 'GEN'}, inplace=True)
df.rename(columns={x3: 'EDU'}, inplace=True)
df.rename(columns={t: 'RAND'}, inplace=True)

for i in range(len(df)): # Distrubute GENDER category Other to Female and Male
    if df.GEN[i] == 3:
        test = np.random.randint(1,2)
        df.GEN[i] = test

# df['GEN'] = df['GEN'].map({1: 'Female', 2: 'Male' })

for i in range(len(df)): # Distrubute AGE category 4 and 5 to 3
    if df.AGE[i] == 4 or df.AGE[i] == 5 :
        df.AGE[i] = 3 

# df['AGE'] = df['AGE'].map({1: '18-24', 2: '25-34', 3: '35+' })

# Distrubute EDU category 1 (< highschool) to 2 (highschool), 4 (Associate Degree) to 5 (Bachelor)
for i in range(len(df)): 
    if df.EDU[i] == 1:
        df.EDU[i] = 2 
    if df.EDU[i] == 4:
        df.EDU[i] = 5 
df.EDU = df.EDU.map({2: 1, 3: 2, 5: 3, 6: 4 })  

# RAND 1 = control, 2 = stock, 3 = timer
df.RAND = df.RAND.map({1: 3, 3:1 })  




a1 = df.loc[df.AGE==1,'BENSUM']
a2 = df.loc[df.AGE==2,'BENSUM']
a3 = df.loc[df.AGE==3,'BENSUM']
a4 = df.loc[df.AGE==4,'BENSUM']
a5 = df.loc[df.AGE==5,'BENSUM']

b1 = df.loc[df.AGE==1,'NASAFRUST']
b2 = df.loc[df.AGE==2,'NASAFRUST']
b3 = df.loc[df.AGE==3,'NASAFRUST']
b4 = df.loc[df.AGE==4,'NASAFRUST']
b5 = df.loc[df.AGE==5,'NASAFRUST']


g1 = df.loc[df.GEN==1,'UXHED']
g2 = df.loc[df.GEN==2,'UXHED']


kwargs = dict(alpha=0.5, bins=5, density=True, cumulative=True)
plt.hist(g1, **kwargs, color='g', label='female')
plt.hist(g2, **kwargs, color='b', label='male')
plt.gca().set(xlabel='UXHED');
plt.legend()


kwargs = dict(alpha=0.5, bins=5, density=True)
plt.hist(g1, **kwargs, color='g', label='female')
plt.hist(g2, **kwargs, color='b', label='male')
plt.gca().set(xlabel='GENDER');
plt.legend()

kwargs = dict(alpha=0.5, bins=100, density=True)
plt.hist(b1, **kwargs, color='k', label='18-24')
plt.hist(b2, **kwargs, color='b', label='25-34')
plt.hist(b3, **kwargs, color='r', label='35-44')
plt.gca().set(xlabel='NASAFRUST');
plt.legend();

kwargs = dict(alpha=0.5, bins=5, density=True, cumulative=True)
plt.hist(a1, **kwargs, color='k', label='18-24')
plt.hist(a2, **kwargs, color='b', label='25-34')
plt.hist(a3, **kwargs, color='r', label='35-44')
plt.gca().set(xlabel='BENSUM');
plt.legend();



model = smf.ols(
    formula='NASAFRUST ~ C(AGE)', data=df).fit(cov_type='HC3')
results = model.summary()
print(results)
aov_table = sm.stats.anova_lm(model, typ=2)
aov_table
stats.shapiro(model.resid)


fig = plt.figure(figsize= (10, 10))
ax = fig.add_subplot(111)

normality_plot, stat = stats.probplot(model.resid, plot= plt, rvalue= True)
ax.set_title("Probability plot of model residual's", fontsize= 20)
ax.set

plt.show()

for x in ('NASASUM','NASAFRUST', 'BENSUM', 'UXPRAG', 'UXHED'):
    for y in ('AGE', 'GEN', 'EDU'):
    # welch anova
        print(x+' '+ y)
        print(pg.welch_anova(dv=x, between=y, data=df))

    # print(stats.kruskal(df[x][df['AGE'] == 1],
    #          df[x][df['AGE'] == 2],
    #          df[x][df['AGE'] == 3]))
    # print(x+' EDU')
    # print(stats.kruskal(df[x][df['EDU'] == 1],
    #          df[x][df['EDU'] == 2],
    #          df[x][df['EDU'] == 3],
    #          df[x][df['EDU'] == 4]))
    # print(x+' GEN')
    # print(stats.kruskal(df[x][df['GEN'] == 1],
    #          df[x][df['GEN'] == 2]))


# regressions

model = smf.ols(
    formula='NASASUM ~ C(RAND) + C(AGE) + C(GEN) + C(EDU)', data=df).fit(cov_type='HC3')
results = model.summary()
print(results)

model = smf.ols(
    formula='NASAFRUST ~ C(RAND) + C(AGE) + C(GEN) + C(EDU)', data=df).fit(cov_type='HC3')
results = model.summary()
print(results)

model = smf.ols(
    formula='BENSUM ~ C(RAND) + C(AGE) + C(GEN) + C(EDU)', data=df).fit(cov_type='HC3')
results = model.summary()
print(results)

model = smf.ols(
    formula='UXPRAG ~ C(RAND) + C(AGE) + C(GEN) + C(EDU)', data=df).fit(cov_type='HC3')
results = model.summary()
print(results)

model = smf.ols(
    formula='UXHED ~ C(RAND) + C(AGE) + C(GEN) + C(EDU)', data=df).fit(cov_type='HC3')
results = model.summary()
print(results)



    
# multiple comparasions
comp = mc.MultiComparison(df.BENSUM, df.AGE)
post_hoc_res = comp.tukeyhsd()
print(post_hoc_res.summary())

post_hoc_res.plot_simultaneous(ylabel= "AGE", xlabel= "Score Difference")

comp = mc.MultiComparison(df.UXHED, df.GEN)
post_hoc_res = comp.tukeyhsd()
print(post_hoc_res.summary())

post_hoc_res.plot_simultaneous(ylabel= "GEN", xlabel= "Score Difference")

# Plot Histogram on x
plt.hist(df["AGE"], bins=5)
plt.gca().set(title='Frequency Histogram', ylabel='age');

# d = Workbook()
# d.save(filename='new_data_timers.xlsx')

# with pd.ExcelWriter('new_data_timers.xlsx', engine="openpyxl", mode='a') as writer:
#     df.to_excel(writer, header=True, index=True, sheet_name='1')