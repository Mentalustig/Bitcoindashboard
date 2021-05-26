#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat May 22 13:50:21 2021
@author: lpeikert
"""

# Import the libraries
import pandas as pd
import numpy as np
import datetime
import yfinance as yf
import math
import nicehash
import pickle

# Initialize dates

startdate = datetime.datetime(2021, 5, 15)
today = datetime.datetime.now()
today = datetime.datetime(today.year, today.month, today.day)
delta = datetime.timedelta(days=1)
delta2 = datetime.timedelta(days=2)

# Read data

staticcapital = pd.read_csv('staticcapital.csv')  
staticcapital['Date'] = pd.to_datetime(staticcapital['Date'], format='%Y-%m-%d')
staticcapital = staticcapital.set_index('Date')

workingcapital = pd.read_csv('workingcapital.csv')  
workingcapital['Date'] = pd.to_datetime(workingcapital['Date'], format='%Y-%m-%d')
workingcapital = workingcapital.set_index('Date')

totalvalue = pd.read_csv('totalvalue.csv')  
totalvalue['Date'] = pd.to_datetime(totalvalue['Date'], format='%Y-%m-%d')
totalvalue = totalvalue.set_index('Date')

kpis = pd.read_csv('kpis.csv')
kpis['Date'] = pd.to_datetime(kpis['Date'], format='%Y-%m-%d')
kpis = kpis.set_index('Date')

staticcapital.loc[today] = [0,0,0,0] if staticcapital.index[-1] != today else print('all good')

workingcapital.loc[today] = [0,0,0,0,0,0,0] if workingcapital.index[-1] != today else print('all good')

totalvalue.loc[today] = [0,0,0,0,0,0,0,0,0,0] if totalvalue.index[-1] != today else print('all good')

kpis.loc[today] = [0,0,0] if kpis.index[-1] != today else print('all good')


# Download Wallet Infos

#OrganizationID = 06ca7b90-1477-40da-b502-596683869ad4
#API Key Code = 02ef110f-6b4a-4269-b206-6f75a291eddd
#API Secret Key Code = b4b1cda2-4c7a-4dc2-9ce7-33be0a12995082494b92-c3f9-4e02-a752-c49d458db8db

### Production  
#API key code: c4c5a286-c2e2-4a61-9094-347001abff3e
#API secret code: f59745af-ffdb-4c52-9ece-793e119d436869cb7c1b-d286-4d92-ae14-052ad06cb39f
#organizationID = 2652eea1-7c24-4350-99d2-7ed86608635a

#TEST
#host = 'https://api-test.nicehash.com'
#organisation_id = '06ca7b90-1477-40da-b502-596683869ad4'
#key = '02ef110f-6b4a-4269-b206-6f75a291eddd'
#secret = 'b4b1cda2-4c7a-4dc2-9ce7-33be0a12995082494b92-c3f9-4e02-a752-c49d458db8db' 

#PROD
host = 'https://api2.nicehash.com'
organisation_id = '2652eea1-7c24-4350-99d2-7ed86608635a'
key = 'c4c5a286-c2e2-4a61-9094-347001abff3e'
secret = 'f59745af-ffdb-4c52-9ece-793e119d436869cb7c1b-d286-4d92-ae14-052ad06cb39f' 


public_api = nicehash.public_api(host)
#buy_info = public_api.buy_info()
#print(buy_info)

private_api = nicehash.private_api(host, organisation_id, key, secret)

my_accounts = private_api.get_accounts_for_currency('BTC')

totalbalance = (my_accounts['totalBalance'])

print('totalBTCbalance =', totalbalance)

activeworkers = private_api.get_active_workers(100, 0, 'RIG_NAME', 'ASC')
activeworkers = activeworkers['workers']

amount_active_rigs = len(activeworkers)
print('amount_active_rigs =', amount_active_rigs)

rigs = pd.DataFrame(list(activeworkers))
rigs['Date'] = today
rigs = rigs.set_index('Date')

getrigIDs = private_api.get_groups_list(True)

rigdata = pd.DataFrame(list(getrigIDs['groups']['']['rigs']))

getrig = []
getrig = pd.DataFrame(getrig, index = rigdata['rigId'])
for i in rigdata['rigId']:
    getrig.at[i, 'name'] = private_api.get_rig2(i)['name']
    getrig.at[i, 'profitability'] = private_api.get_rig2(i)['profitability']


rigdata = rigdata.set_index('rigId')

for i in rigdata.index:
    for o in range(0, 6):
        basename = "powerusage"
        columnname = basename + "_" + str(o+1)
        try:
            getrig.at[i, columnname] = private_api.get_rig2(i)['devices'][o]['powerUsage']
        except IndexError:
          #  getrig.at[i, columnname] = 'null'
            print('Oops, I did not find power usage for', i)



dailyprofitability = getrig['profitability'].sum()

powerlist= list(getrig)
powerlist.remove('name')
powerlist.remove('profitability')

getrig['totalpowerusage'] = getrig[powerlist].sum(axis=1)
totalpowerusage = (getrig['totalpowerusage'].sum(axis=0)/1000)*24

getrig = pd.concat([getrig, rigdata['status']], axis=1)
getrig = pd.concat([getrig, rigdata['totalDevices']], axis=1)
getrig = pd.concat([getrig, rigdata['activeDevices']], axis=1)



"""
NOT NEEDED ANYMORE
# Download market data
df_yahoo_BTCUSD = yf.download('BTC-USD', start='2021-05-15', progress='False')
df_yahoo_BTCUSD = df_yahoo_BTCUSD['Adj Close']
df_yahoo_USDAED = yf.download('AED=X', start='2021-05-15', progress='False')
df_yahoo_USDAED = df_yahoo_USDAED['Adj Close']
# initialize list of lists
wc = pd.concat([df_yahoo_BTCUSD, df_yahoo_USDAED], axis=1)
wclist = [[0, 0, 0, 0]]
workingcapital = pd.DataFrame(wclist)
workingcapital = pd.concat([wc, workingcapital], axis=1)
workingcapital.columns = ['Exchange Rate BTC/USD', 'Exchange Rate USD/AED', 'Amount BTC', 'Electricity Costs', 'Total Electricity Costs', 'Money taken out']
workingcapital.index.names = ['Date']
workingcapital = workingcapital.iloc[1:]
while startdate <= today :
    if math.isnan(workingcapital['Exchange Rate USD/AED'][startdate]) :
        workingcapital['Exchange Rate USD/AED'][startdate] = workingcapital['Exchange Rate USD/AED'][startdate-delta]
        if math.isnan(workingcapital['Exchange Rate USD/AED'][startdate-delta]) :
            workingcapital['Exchange Rate USD/AED'][startdate] = workingcapital['Exchange Rate USD/AED'][startdate-delta2]
    startdate += delta
startdate = datetime.datetime(2021, 5, 15)
df_ER_BTCUSD = workingcapital['Exchange Rate BTC/USD']*workingcapital['Exchange Rate USD/AED']
df_ER_BTCUSD = pd.DataFrame(df_ER_BTCUSD, columns = ['Exchange Rate BTC/AED'])
workingcapital = pd.concat([df_ER_BTCUSD, workingcapital], axis=1)
staticcapital = workingcapital.copy()
staticcapital[['Amount Invested', 'Amount Reinvested', 'Depreciation Rigs', 'Total Value Rigs']] = ['','','','']
staticcapital = staticcapital[['Amount Invested', 'Amount Reinvested', 'Depreciation Rigs', 'Total Value Rigs']]
totalvalue = workingcapital.copy()
totalvalue[['Total invested', 'Total Value', 'Total Gain', 'Total Daily Gain', '%Total Gain', '%Daily Gain', '% cummulating p.a.', '% average p.a.', '']] = ['', '', '', '', '', '', '', '', '']
totalvalue = totalvalue[['Total invested', 'Total Value', 'Total Gain', 'Total Daily Gain', '%Total Gain', '%Daily Gain', '% cummulating p.a.', '% average p.a.', '']]
kpis = workingcapital.copy()
kpis[['Productivity per rig', 'Daily productivity', 'Average productivity']] = ['', '', '']
kpis = kpis[['Productivity per rig', 'Daily productivity', 'Average productivity']]
"""

#clean up all float type integers

staticcapital["Amount Invested"] = pd.to_numeric(staticcapital["Amount Invested"], downcast="float")
staticcapital["Total Value Rigs"] = pd.to_numeric(staticcapital["Total Value Rigs"], downcast="float")
workingcapital['Amount BTC'] = pd.to_numeric(workingcapital['Amount BTC'], downcast="float")
totalvalue["% average p.a."] = pd.to_numeric(totalvalue["% average p.a."], downcast="float")
totalvalue["% cummulating p.a."] = pd.to_numeric(totalvalue["% cummulating p.a."], downcast="float")
totalvalue["%Total Gain"] = pd.to_numeric(totalvalue["%Total Gain"], downcast="float")

#what did I invest
staticcapital['Amount Invested'][datetime.datetime(2021, 5, 26)] = 150000


"""
NOT NEEDED ANYMORE
# when did we buy rigs
staticcapital['Amount Invested'][datetime.datetime(2021, 5, 15)] = 10000
staticcapital['Amount Invested'][datetime.datetime(2021, 5, 20)] = 30000
staticcapital['Amount Invested'][datetime.datetime(2021, 5, 22)] = 70000
staticcapital['Amount Invested'][datetime.datetime(2021, 5, 26)] = 150000

for i in range (0, int(((today-startdate).days)+2)):
    try:
        workingcapital.iloc[i, 5] = workingcapital.iloc[:i+1, 4].sum()
    except IndexError:
        print('Oops, I did not find any electricity data')
# calculate how much depreciation we incur
depreciation = float(-1/(365*5))
totalvalue['Total Gain'] = totalvalue['Total Value'] - totalvalue['Total invested']
totalvalue['%Total Gain'] = (totalvalue['Total Gain']/totalvalue['Total invested'])*100
for i in range (0, int(((today-startdate).days)+2)):
    if totalvalue.iloc[i, 0] != 0:
        totalvalue.iloc[i, 6] = ((totalvalue.iloc[i, 2]/totalvalue.iloc[i, 0] +1 ) ** (365/i) -1) * 100
for i in range (0, int(((today-startdate).days)+2)):
    if totalvalue.iloc[i, 0] != 0:
        totalvalue.iloc[i, 7] = ((totalvalue.iloc[i, 2]/totalvalue.iloc[i, 0]) * (365/i)) * 100
for i in range (0, int(((today-startdate).days)+2)):
    try:
        staticcapital.iloc[i, 2] = staticcapital.iloc[:i+1, 0].sum() * depreciation
    except IndexError:
        print('Oops, I did not find any more days', i)
for i in range (0, int(((today-startdate).days)+2)):
    try:
        staticcapital.iloc[i, 3] = staticcapital.iloc[:i+1, 0].sum()+staticcapital.iloc[:i+1, 2].sum()
    except IndexError:
        print('Oops, I made a mistake for value rigs calculation')
# Getting overall value
for i in range (0, int(((today-startdate).days)+2)):
    try:
        totalvalue.iloc[i, 0] = staticcapital.iloc[:i+1, 0].sum()
    except IndexError:
        print('Oops, I made a mistake for total invested calculation')
for i in range (0, int(((today-startdate).days)+2)):
    try:
        # totalvalue = rig value + btc value + electricity costs accumulated + 
        totalvalue.iloc[i, 1] = staticcapital.iloc[i, 3]+(0 if math.isnan(workingcapital.iloc[i, 3]) else workingcapital.iloc[i, 3]*workingcapital.iloc[i,0])+workingcapital.iloc[i, 5]
    except IndexError:
        print('Oops, I made a mistake for total invested calculation')
staticcapital.to_pickle("staticcapital.pkl")  # saved old dataframes
workingcapital.to_pickle("workingcapital.pkl")  # saved old dataframes
totalvalue.to_pickle("totalvalue.pkl")  # saved old dataframes
kpis.to_pickle("kpis.pkl")  # saved old dataframes
"""


"""
INSERT CODE TO GET NEW VALUES FROM THE YAHOO API
"""

# Download market data

df_yahoo_BTCUSD = yf.download('BTC-USD', start=startdate, progress='False')
df_yahoo_BTCUSD = df_yahoo_BTCUSD['Adj Close']

df_yahoo_USDAED = yf.download('AED=X', start=startdate, progress='False')
df_yahoo_USDAED = df_yahoo_USDAED['Adj Close']



workingcapital['Exchange Rate BTC/USD'][today] = df_yahoo_BTCUSD.iloc[-1]

if df_yahoo_USDAED.iloc[-1] > 0:
    workingcapital['Exchange Rate USD/AED'][today] = df_yahoo_USDAED.iloc[-1]
else:
    workingcapital['Exchange Rate USD/AED'][today] = workingcapital.iloc[-2,2]

workingcapital['Exchange Rate BTC/AED'][today] = workingcapital.iloc[-1, 1]*workingcapital.iloc[-1, 2]


"""
DID WE BUY NEW RIGS?
"""
# when did we buy rigs
#staticcapital['Amount Invested'][datetime.datetime(YEAR, MONTH, DAY)] = SUMME INVESTED


"""
INSERT CODE TO GET NEW VALUES FROM RIGS & make tables up to date
"""

workingcapital['Amount BTC'][today] = float(totalbalance)
kpis['Daily productivity'][today] = float(dailyprofitability)
kpis['Average productivity'][today] = float(workingcapital['Amount BTC'][today]/int((today-startdate).days))
kpis['Active Rigs'] = 0
kpis['Active Rigs'][today] = int(getrig.status[getrig.status == 'MINING'].count())

cost_elec_per_rig_per_watt = 0.36
workingcapital['Electricity Costs'][today] = cost_elec_per_rig_per_watt*totalpowerusage


try:
    workingcapital.iloc[-1, 5] = workingcapital.iloc[:, 4].sum()
except IndexError:
    print('Oops, I did not find any electricity data')

depreciation = -1/(365*5)

try:
    staticcapital.iloc[-1, 2] = staticcapital.iloc[:, 0].sum() * depreciation
except IndexError:
    print('Oops, I did not find any more days')
    
try:
    staticcapital.iloc[-1, 3] = staticcapital.iloc[:, 0].sum()+staticcapital.iloc[:, 2].sum()
except IndexError:
    print('Oops, I made a mistake for value rigs calculation')

# Getting overall value
try:
    totalvalue.iloc[-1, 0] = staticcapital.iloc[:, 0].sum()
except IndexError:
    print('Oops, I made a mistake for total invested calculation')


try:
    # totalvalue = rig value + btc value + electricity costs accumulated + 
    totalvalue.iloc[-1, 1] = staticcapital.iloc[-1, 3]+(0 if math.isnan(workingcapital.iloc[-1, 3]) else workingcapital.iloc[-1, 3]*workingcapital.iloc[-1,0])+workingcapital.iloc[-1, 5]
except IndexError:
    print('Oops, I made a mistake for total invested calculation')
    
totalvalue['Total Gain'] = totalvalue['Total Value'] - totalvalue['Total invested']
totalvalue['Total Daily Gain'] = totalvalue['Total Gain'] - totalvalue['Total Gain'].shift(1)
totalvalue['%Daily Gain'] = (totalvalue['Total Daily Gain']/totalvalue['Total invested']) * 100
totalvalue['%Total Gain'] = (totalvalue['Total Gain']/totalvalue['Total invested']) * 100
totalvalue.iloc[-1, 6] = ((totalvalue.iloc[-1, 2]/totalvalue.iloc[-1, 0] +1 ) ** (365/(today-startdate).days) -1) * 100
totalvalue.iloc[-1, 7] = ((totalvalue.iloc[-1, 2]/totalvalue.iloc[-1, 0]) * (365/(today-startdate).days)) * 100

totalvalue['% cummulative p.a. using average productivity'] = ((((kpis['Average productivity']*workingcapital['Exchange Rate BTC/AED']-staticcapital['Depreciation Rigs']-workingcapital['Electricity Costs'])*30)/totalvalue.iloc[:, 0] +1 ) ** (365/30) -1) * 100
totalvalue['% cummulative p.a. using daily productivity'] = ((((kpis['Daily productivity']*workingcapital['Exchange Rate BTC/AED']-staticcapital['Depreciation Rigs']-workingcapital['Electricity Costs'])*30)/totalvalue.iloc[:, 0] +1 ) ** (365/30) -1) * 100

# Save data into new data sets

getrig.to_csv("getrig.csv", index=True)
staticcapital.to_csv("staticcapital.csv", index=True)
workingcapital.to_csv("workingcapital.csv", index=True)
totalvalue.to_csv("totalvalue.csv", index=True)
kpis.to_csv("kpis.csv", index=True)
