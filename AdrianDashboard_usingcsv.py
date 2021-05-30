#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 10:06:29 2021
@author: lpeikert
"""
import streamlit as st 
import pandas as pd
import numpy as np
import pickle
import altair as alt

staticcapital = pd.read_csv('https://raw.githubusercontent.com/Mentalustig/Bitcoindashboard/main/staticcapital.csv')  
staticcapital['Date'] = pd.to_datetime(staticcapital['Date'], format='%Y-%m-%d')
staticcapital = staticcapital.set_index('Date')

workingcapital = pd.read_csv('https://raw.githubusercontent.com/Mentalustig/Bitcoindashboard/main/workingcapital.csv')  
workingcapital['Date'] = pd.to_datetime(workingcapital['Date'], format='%Y-%m-%d')
workingcapital = workingcapital.set_index('Date')

totalvalue = pd.read_csv('https://raw.githubusercontent.com/Mentalustig/Bitcoindashboard/main/totalvalue.csv')  
totalvalue['Date'] = pd.to_datetime(totalvalue['Date'], format='%Y-%m-%d')
totalvalue = totalvalue.set_index('Date')

kpis = pd.read_csv('https://raw.githubusercontent.com/Mentalustig/Bitcoindashboard/main/kpis.csv')
kpis['Date'] = pd.to_datetime(kpis['Date'], format='%Y-%m-%d')
kpis = kpis.set_index('Date')

getrig = pd.read_csv('https://raw.githubusercontent.com/Mentalustig/Bitcoindashboard/main/getrig.csv')



st.set_page_config(page_title = 'Streamlit Dashboard', layout='wide', page_icon='💹')
st.header('Adrians BTC Dashboard')

st.button('I am just a gimmick button but lucas did not program me yet')

### top row 

st.markdown("## Main KPIs")
st.markdown(f"as of {totalvalue.index[-1]}")


first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi, seventh_kpi, eigth_kpi, nineth_kpi, tenth_kpi = st.beta_columns(10)


with first_kpi:
    st.markdown("**Total Gain in AED**")
    number1 = int(totalvalue.iloc[-1,2])
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Total Gain in %**")
    number2 = round((totalvalue.iloc[-1,4]),1)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Daily Gain in AED**")
    number3 = int(totalvalue.iloc[-1,3])
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number3}</h1>", unsafe_allow_html=True)
    
with fourth_kpi:
    st.markdown("**Daily Gain in %**")
    number4 = round(totalvalue.iloc[-1,5],2)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number4}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**Average prod. BTC**")
    number5 = round(kpis.iloc[-1,2],4)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number5}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown("**Daily prod. BTC vs actual**")
    number6 = str(round(kpis.iloc[-1,1],4))+'vs'+str(round(workingcapital.iloc[-1,7],4))
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number6}</h1>", unsafe_allow_html=True)
    
with seventh_kpi:
    st.markdown("**Active Rigs**")
    number7 = str(getrig.status[getrig.status == 'MINING'].count())+'  / '+str(getrig.status.count()) 
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number7}</h1>", unsafe_allow_html=True)
    
with eigth_kpi:
    st.markdown("**Mio in (avg. gain)**")
    number8 = str(int(1000000/(totalvalue.iloc[-1,2]/len(totalvalue.iloc[:,3]))/365))+' years'
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number8}</h1>", unsafe_allow_html=True)

with nineth_kpi:
    st.markdown("**Mio in (daily gain)**")
    number9 = str(int(1000000/totalvalue.iloc[-1,3]/365))+' years'
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number9}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)




namesactiverigs = ':'
namesinactiverigs = ':'
#st.markdown("## Mining Rig KPIs Trial 2")
for i in (range(0,getrig.status.count())):
    if getrig.status[i]=='MINING':
        namesactiverigs += ' '+str(getrig.name.iloc[i])
    else:
        namesinactiverigs += ' '+str(getrig.name.iloc[i])
        

st.markdown(f"Running :white_check_mark: {namesactiverigs} and  :red_circle: **OFFLINE :x: {namesinactiverigs}**")

st.markdown("<hr/>", unsafe_allow_html=True)

st.markdown("Active vs. Total Devices and Daily BTC")

first_chart, second_chart = st.beta_columns(2)

with first_chart:
    chart_data = getrig.iloc[:,-2:]
    st.area_chart(chart_data)

with second_chart:
    chart_data = workingcapital['Daily BTC']
    st.area_chart(chart_data)


st.markdown("<hr/>", unsafe_allow_html=True)



#st.markdown("## Mining Rig KPIs Trial 3")
st.markdown("Profitability per rig")
st.bar_chart(getrig.profitability)

st.markdown("Total power usage per rig")
st.bar_chart(getrig.totalpowerusage)




st.markdown("Total Gain and Total Value vs Invested")

first_chart, second_chart = st.beta_columns(2)

with first_chart:
    chart_data = totalvalue[['Total Gain', 'Total Daily Gain']]
    st.line_chart(chart_data)

     
with second_chart:
    df = totalvalue
    df.reset_index(drop=True, inplace=True)
    chart_data = df[['Total Value', 'Total invested']]
    st.area_chart(chart_data)

   
st.markdown("<hr/>", unsafe_allow_html=True)
st.markdown("forecast yearly return")

 
first_chart, second_chart = st.beta_columns(2)

with first_chart:
    chart_data = totalvalue[['% cummulating p.a.', '% average p.a.', '% cummulative p.a. using average productivity', '% cummulative p.a. using daily productivity']]
    st.line_chart(chart_data)


with second_chart:
    chart_data = workingcapital['Exchange Rate BTC/AED']
    st.area_chart(chart_data)



st.markdown("<hr/>", unsafe_allow_html=True)

st.markdown("Total Value")
st.dataframe(totalvalue)
#st.table(totalvalue)

st.markdown("workingc apital")
st.dataframe(workingcapital)

st.markdown("static capital")
st.dataframe(staticcapital)

st.markdown("rig data")
st.dataframe(getrig)



"""
#Analysis
"""
# Sensitivity Analysis

#sensitivityrates = np.array([0.05, 0.15, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 1.85, 1.95])
dailyprofitability = kpis.iloc[-1,1]


sensitivityrates = np.arange(0.2, 2, 0.2)
sensitivityrates2 = np.arange(0.6, 1.5, 0.1)
rateBTCAED = sensitivityrates * (workingcapital.iloc[-1, 0])
rateprofitability = sensitivityrates * dailyprofitability

parameters = []
paras = []
parameters = pd.DataFrame(parameters, columns = rateBTCAED, index = rateprofitability)
for i in rateBTCAED:
    for o in rateprofitability:
        parameters[o, i] = (((((i*o-workingcapital.iloc[-1,4])*30)/totalvalue.iloc[-1,0])+1)**(365/30)-1)
        paras.append(((((i*o*30)/totalvalue.iloc[-1,0])+1)**(365/30)-1))

rateBTCAEDlist = 100 * np.repeat(sensitivityrates,len(sensitivityrates))
rateprofitabilitylist = 100 * np.tile(sensitivityrates2,len(sensitivityrates2))
heatmap = pd.DataFrame({'values': paras, 'exchange rate BTCAED %': rateBTCAEDlist, 'profitability rate %': rateprofitabilitylist})

import seaborn as sns
import matplotlib.pyplot as plt

pvt = pd.pivot_table(pd.DataFrame(heatmap),
    values='values', index='exchange rate BTCAED %', columns='profitability rate %')
ax = sns.heatmap(pvt, annot=True, annot_kws={"size": 7}, vmax = 3, cmap="YlGnBu")

st.write(ax)
st.pyplot()














""" 

OLD UNUSED CODE

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi, seventh_kpi = st.beta_columns(7)


with first_kpi:
    st.markdown(f"**{getrig.name[0]} : {getrig.status[0]} {getrig.name[1]} : {getrig.status[1]}**")
    chart_data = getrig.iloc[0,-2:]
    st.bar_chart(chart_data)

with second_kpi:
    st.markdown(f"**{getrig.name[1]} : {getrig.status[1]} {getrig.name[1]} : {getrig.status[1]}**")
    chart_data = getrig.iloc[1,-2:]
    st.bar_chart(chart_data)

with third_kpi:
    st.markdown(f"**{getrig.name[2]} : {getrig.status[2]}        {getrig.name[3]} : {getrig.status[3]}**")
    chart_data = getrig.iloc[2,-2:]
    st.bar_chart(chart_data)
    
with fourth_kpi:
    st.markdown(f"**{getrig.name[4]} : {getrig.status[4]}        {getrig.name[5]} : {getrig.status[5]}**")
    chart_data = getrig.iloc[3,-2:]
    st.bar_chart(chart_data)

with fifth_kpi:
    st.markdown(f"**{getrig.name[6]} : {getrig.status[6]}        {getrig.name[7]} : {getrig.status[7]}**")
    chart_data = getrig.iloc[4,-2:]
    st.bar_chart(chart_data)

with sixth_kpi:
    st.markdown(f"**{getrig.name[8]} : {getrig.status[8]}        {getrig.name[9]} : {getrig.status[9]}**")
    chart_data = getrig.iloc[5,-2:]
    st.bar_chart(chart_data)

with seventh_kpi:
    st.markdown(f"**{getrig.name[10]} : {getrig.status[10]}        {getrig.name[1]} : {getrig.status[1]}**")
    chart_data = getrig.iloc[6,-2:]
    st.bar_chart(chart_data)

st.markdown("## Mining Rig KPIs")

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi, seventh_kpi, eigth_kpi, nineth_kpi = st.beta_columns(9)


with first_kpi:
    st.markdown(f"**{getrig.name[0]} : {getrig.status[0]} active/totaldevices**")
    number1 = [getrig.activeDevices[0], getrig.totalDevices[0]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown(f"**{getrig.name[1]} : {getrig.status[1]} active/totaldevices**")
    number2 = [getrig.activeDevices[1], getrig.totalDevices[1]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown(f"**{getrig.name[2]} : {getrig.status[2]} active/totaldevices**")
    number3 = [getrig.activeDevices[2], getrig.totalDevices[2]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number3}</h1>", unsafe_allow_html=True)
    
with fourth_kpi:
    st.markdown(f"**{getrig.name[3]} : {getrig.status[3]} active/totaldevices**")
    number4 = [getrig.activeDevices[3], getrig.totalDevices[3]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number4}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown(f"**{getrig.name[4]} : {getrig.status[4]} active/totaldevices**")
    number5 = [getrig.activeDevices[4], getrig.totalDevices[4]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number5}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown(f"**{getrig.name[5]} : {getrig.status[5]} active/totaldevices**")
    number6 = [getrig.activeDevices[5], getrig.totalDevices[5]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number6}</h1>", unsafe_allow_html=True)

with seventh_kpi:
    st.markdown(f"**{getrig.name[6]} : {getrig.status[6]} active/totaldevices**")
    number7 = [getrig.activeDevices[6], getrig.totalDevices[6]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number7}</h1>", unsafe_allow_html=True)

with eigth_kpi:
    st.markdown(f"**{getrig.name[7]} : {getrig.status[7]} active/totaldevices**")
    number8 = [getrig.activeDevices[7], getrig.totalDevices[7]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number8}</h1>", unsafe_allow_html=True)

with nineth_kpi:
    st.markdown(f"**{getrig.name[8]} : {getrig.status[8]} active/totaldevices**")
    number9 = [getrig.activeDevices[8], getrig.totalDevices[8]]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number9}</h1>", unsafe_allow_html=True)
    
st.markdown("<hr/>", unsafe_allow_html=True)



first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi, seventh_kpi, eigth_kpi, nineth_kpi = st.beta_columns(9)

with first_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number1 = [round(1000*getrig.profitability[0],2), int(getrig.totalpowerusage[0])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number2 = [round(1000*getrig.profitability[1],2), int(getrig.totalpowerusage[1])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number3 = [round(1000*getrig.profitability[2],2), int(getrig.totalpowerusage[2])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number3}</h1>", unsafe_allow_html=True)
    
with fourth_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number4 = [round(1000*getrig.profitability[3],2), int(getrig.totalpowerusage[3])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number4}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number5 = [round(1000*getrig.profitability[4],2), int(getrig.totalpowerusage[4])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number5}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number6 = [round(1000*getrig.profitability[5],2), int(getrig.totalpowerusage[5])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number6}</h1>", unsafe_allow_html=True)

with seventh_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number7 = [round(1000*getrig.profitability[6],2), int(getrig.totalpowerusage[6])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number7}</h1>", unsafe_allow_html=True)

with eigth_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number8 = [round(1000*getrig.profitability[7],2), int(getrig.totalpowerusage[7])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number8}</h1>", unsafe_allow_html=True)

with nineth_kpi:
    st.markdown("**prof*1000 / powerusage**")
    number9 = [round(1000*getrig.profitability[8],2), int(getrig.totalpowerusage[8])]
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number9}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)


"""