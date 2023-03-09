#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 28 11:01:53 2022

@author: reha.tuncer
"""
import pandas as pd
import difflib
import numpy as np

pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)
"""
Get text to check
"""
captchas = pd.read_excel("captchas_list.xlsx", "captchas", header=None)

"""
Get participant input
"""
db = pd.read_csv('participants_v2.csv')

"""
Filter participants by ID
"""
# db = db[db.ID.isin(['6017f6742d7cc9ad4f98fb4d',
#                     '6145e674f74f637530a08a39',
#                     '62cfeab06cb6c36b80b91493',
#                     '613f1d6420141eefc3e5f1b0',
#                     '55d4c46f58c35800113dc131',
#                     '60ac08be37cd5e98ab2d0037',
#                     '5bdcf08f05ed110001ab2bbf',
#                     '58a17caf6a8d3b00017ec00e',
#                     '5b7e7de287d85f0001bac19a',
#                     '5642444817bdbe00062a1129',
#                     '59b555702a78fd00010b86d4',
#                     '5cd47eac121337001afb9e96',
#                     '5c366fc38821900001b38b67',
#                     '5bf50c187ea49f0001ba734a',
#                     '608fdbc4196e5708ed3f291a',
#                     '5efde724d80f81077c0800b9'
#                     ])]


# db = db[93:] # start of second wave in DB (1st of march)

# db = db[db.ID.str.len()>20] # drop test entries shorter than prolific id's

"""
Drop participants who did not finish 
"""
noapprove = db[db['browser.birthyear'].isnull()]
db = db[~db['browser.birthyear'].isnull()]  # drop empty entries
db = db.reset_index(drop=True)
for i in range(len(db)):
    if type(db['browser.userTranscription'][i]) is float:
        db['browser.userTranscription'][i] = str(np.nan)
    # if db["treatment"][i] != "MPL":  # reset MPL by treatment
    #     db["browser.MPLthatcounts"][i] = str(np.nan)

"""
Drop failed attention checks
"""
failcheck = db[(db['attention1']+db['attention2']) >= 4]
db = db[(db['attention1']+db['attention2']) < 4]  # drop more than 4 mistake
db = db.reset_index(drop=True)


# """
# Get MPL bonus if treatment is MPL
# """
# s = '+'
# e = '£'
# MPL = []
# MPLcondition = []
# MPLid = []
# for i in range(len(db)):
#     MPLid.append(db["ID"][i])
#     if db["treatment"][i] == 'MPL':
#         MPLcondition.append(db["browser.MPLthatcounts"][i].split(s)[
#                             0])  # get autoplay condition but work on merge

#         MPL.append(float((db["browser.MPLthatcounts"]
#                     [i].split(s))[1].split(e)[0]))
#     else:
#         MPLcondition.append(str(np.nan))
#         MPL.append(float(0))

# MPL = pd.DataFrame([MPLid, MPLcondition, MPL])
# MPL = MPL.transpose()
# MPL = MPL.rename(
#     columns={0: "ID"})
"""
Typing analysis
"""
text = []
for i in range(len(db)):
    text.append(db['browser.userTranscription'][i].split(','))

text = pd.DataFrame(text).transpose()

allscore = pd.DataFrame(text)
accuracy = []

for y in range(len(text.columns)):
    for x in range(len(text[y])):
        if text[y][x] is not None:
            for i in range(len(captchas[0])):
                accuracy.append(difflib.SequenceMatcher(
                    None, text[y][x], captchas[0][i]).ratio())
            allscore[y][x] = max(accuracy)
            accuracy = []
t = []
v = []
for i in range(len(allscore.columns)):
    t.append(sum(filter(None, allscore[i])))
    v.append(allscore[i].count(None))  # completed sentences!
    t[i] = t[i]/v[i]
    t[i] = t[i].round(4)*100

# sentences per minute spent typing
permin = (v/(db["browser.timespentTyping"]/60)).round(2)
pcentacc = pd.DataFrame(t).rename(
    columns={0: "accuracy"})  # percent typing accuracy

"""
Bonus Payments
"""

watchTime = pd.DataFrame(db["browser.timespentWatching"] -
                         db["browser.videoPausedFor"]-
                         db["browser.timespentNotWatching"]).rename(columns={0: "watchTime"})
typeTime = pd.DataFrame(db["browser.timespentTyping"] -
                        db["browser.timespentNotTyping"]).rename(columns={0: "typeTime"})
payment = pd.concat(
    [watchTime,
     typeTime], axis=1)

# add 2 seconds because of db mistake, 0.5 per sec
payment.watchTime = (payment.watchTime + 2)*0.2
payment.typeTime = payment.typeTime * 0.1  # 0.1 per sec

# check for accuracy and permin conditions
for i in range(len(db)):
    if (permin[i] < 0.9) or (pcentacc["accuracy"][i] < 70):
        payment.typeTime[i] = 0
# because mean-std was around 0.9 and not 1 for permin
payment

"""
Payment Output Table
"""
total = []
for i in range(len(payment)):
    # sum over 2 tasks and convert to pounds
    total.append(round((sum(payment.iloc[i]))/100, 2))

total = pd.DataFrame(total)
total = total.rename(columns={0: "bonus"})
total = pd.concat([total, db["ID"], db["treatment"],
                  db["browser.name"],
                  watchTime,
                  typeTime,
                  db["timeChoice"],
                  db["lottery"],
                  pd.DataFrame(permin).rename(
                      columns={"browser.timespentTyping": "permin"}),
                  pcentacc
                   ], axis=1)

total = total[~total['lottery'].str.contains(
    "lotteryWin")]  # drop lotteryWin entries
total['pType'] = pd.DataFrame(((total.typeTime)/720)*100).round(2)
total['diff'] = pd.DataFrame(total['timeChoice']-total['pType'])

print(total)

# total = total.merge(MPL, on="ID")
# total['total'] = total["bonus"]+MPL[2]
# total["bonus"] = total["bonus"]+MPL[2]-2  # add MPL and remove base payment

# for i in range(len(total)):
#     if total.bonus[i] < 0:
#         total["bonus"][i] = 0
# if total["total"][i] < 2:
#     total["total"][i] = 2

