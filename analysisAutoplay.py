#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 11:05:19 2023

@author: reha.tuncer
"""
import pandas as pd
# import difflib
import numpy as np
# import matplotlib.pyplot as plt
import seaborn as sns


pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)
pd.set_option('display.max_columns', None)


"""
Get data
"""
db0 = pd.read_csv('participants.csv')
# clean initial database
db0 = db0[93:]  # start of second wave in DB (1st of march)
# drop test entries shorter than prolific id's
db0 = db0[db0.ID.str.len() > 20]

db = pd.read_csv('participants_v2.csv')


"""
Drop participants who did not finish 
"""
noapprove = db[db['browser.birthyear'].isnull()]
db = db[~db['browser.birthyear'].isnull()]  # drop empty entries
db = db.reset_index(drop=True)
for i in range(len(db)):
    if type(db['browser.userTranscription'][i]) is float:
        db['browser.userTranscription'][i] = str(np.nan)

db0 = db0[~db0['browser.birthyear'].isnull()]  # drop empty entries
db0 = db0.reset_index(drop=True)
for i in range(len(db0)):
    if type(db0['browser.userTranscription'][i]) is float:
        db0['browser.userTranscription'][i] = str(np.nan)


"""
Drop failed attention checks
"""
failcheck = db[(db['attention1']+db['attention2']) >= 4]
db = db[(db['attention1']+db['attention2']) < 4]  # drop more than 4 mistake
db = db.reset_index(drop=True)

db0 = db0[(db0['attention1']+db0['attention2'])
          < 4]  # drop more than 4 mistake
db0 = db0.reset_index(drop=True)

"""
Check for bad connection
"""
badconnection = db[db['browser.connection'].str.contains(
    "Bad")]  # drop bad connection entries
db = db[~db['browser.connection'].str.contains(
    "Bad")]
db = db.reset_index(drop=True)


"""
Drop time choice binding
"""

db = db[~db['lottery'].str.contains(
    "lotteryWin")]  # drop lotteryWin entries

db0 = db0[~db0['lottery'].str.contains(
    "lotteryWin")]

"""
Correct for actual time spent on task
"""

db["watchTime"] = pd.DataFrame(db["browser.timespentWatching"] -
                               # db["browser.videoPausedFor"] -
                               db["browser.timespentNotWatching"]).rename(columns={0: "watchTime"})
db["typeTime"] = pd.DataFrame(db["browser.timespentTyping"] -
                              db["browser.timespentNotTyping"]).rename(columns={0: "typeTime"})


db['pType'] = pd.DataFrame(((db["typeTime"])/720)*100).round(2)
db['pTypeChoice'] = pd.DataFrame(((db["timeChoice"])/720)*100).round(2)
db['diff'] = pd.DataFrame(db['pTypeChoice']-db['pType'])


db0["watchTime"] = pd.DataFrame(db0["browser.timespentWatching"] -
                                db0["browser.videoPausedFor"] -
                                db0["browser.timespentNotWatching"]).rename(columns={0: "watchTime"})
db0["typeTime"] = pd.DataFrame(db0["browser.timespentTyping"] -
                               db0["browser.timespentNotTyping"]).rename(columns={0: "typeTime"})


db0['pType'] = pd.DataFrame(((db0["typeTime"])/720)*100).round(2)
db0['pTypeChoice'] = pd.DataFrame(((db0["timeChoice"])/720)*100).round(2)
db0['diff'] = pd.DataFrame(db0['pTypeChoice']-db0['pType'])


"""
Graphs
"""

# sns.set_theme(style="whitegrid")

# sns.kdeplot(
#     db, cumulative=True, common_norm=False, common_grid=True,
#     x="typeTime", hue="treatment",
# )
# sns.kdeplot(
#     db, cumulative=True, common_norm=False, common_grid=True,
#     x="watchTime", hue="treatment",
# )
# sns.displot(db, x="typeTime",
#             kind="kde", hue="treatment")

# sns.displot(db, x="watchTime",
#             kind="kde", hue="treatment")s

# sns.histplot(db, x="typeTime", hue="treatment")
# sns.histplot(db, x="watchTime", hue="treatment")

# sns.catplot(db, x="watchTime", y="treatment",
#             kind="violin", bw=.25, cut=0, split=True)
# sns.catplot(db, x="browser.tabCounter", y="treatment",
#             kind="violin", bw=.25, cut=0, split=True)

sns.catplot(db, x="typeTime", y="treatment", kind="boxen")
sns.catplot(db, x="watchTime", y="treatment", kind="boxen")
sns.catplot(db, x="browser.watchedVideo", y="treatment", kind="boxen")
sns.catplot(db, x="browser.watchedVideo", y="treatment")
sns.catplot(db, x="watchTime", y="treatment", kind="swarm")

sns.catplot(db0, x="browser.watchedVideo", y="treatment", kind="boxen")
sns.catplot(db0, x="typeTime", y="treatment", kind="boxen")
sns.catplot(db0, x="watchTime", y="treatment", kind="boxen")


"""
People who watched videos
"""
np.average(db0.watchTime[db0["browser.watchedVideo"]
           > 4][db0.treatment == "autoplayOn"])
np.average(db0.watchTime[db0.watchTime > 60][db0.treatment == "autoplayOff"])
np.average(db.watchTime[db.watchTime > 60][db.treatment == "autoplayOn"])
np.average(db.watchTime[db.watchTime > 60][db.treatment == "autoplayOff"])
np.average(db.watchTime[db.treatment == "autoplayOn"])
np.average(db.watchTime[db.treatment == "autoplayOff"])
sns.displot(db0[db0.watchTime > 100], x="watchTime", hue="treatment")

db.watchTime[db.watchTime < 100][db.treatment == "autoplayOn"].count()
db.watchTime[db.watchTime < 100][db.treatment == "autoplayOff"].count()
