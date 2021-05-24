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

staticcapital = pd.read_csv('/Users/lpeikert/Desktop/rest-clients-demo-master/python/staticcapital.csv')  
staticcapital['Date'] = pd.to_datetime(staticcapital['Date'], format='%Y-%m-%d')
staticcapital = staticcapital.set_index('Date')

workingcapital = pd.read_csv('/Users/lpeikert/Desktop/rest-clients-demo-master/python/workingcapital.csv')  
workingcapital['Date'] = pd.to_datetime(workingcapital['Date'], format='%Y-%m-%d')
workingcapital = workingcapital.set_index('Date')

totalvalue = pd.read_csv('/Users/lpeikert/Desktop/rest-clients-demo-master/python/totalvalue.csv')  
totalvalue['Date'] = pd.to_datetime(totalvalue['Date'], format='%Y-%m-%d')
totalvalue = totalvalue.set_index('Date')

kpis = pd.read_csv('/Users/lpeikert/Desktop/rest-clients-demo-master/python/kpis.csv')
kpis['Date'] = pd.to_datetime(kpis['Date'], format='%Y-%m-%d')
kpis = kpis.set_index('Date')



st.set_page_config(page_title = 'Streamlit Dashboard', layout='wide', page_icon='💹')
st.header('Adrians BTC Dashboard')

st.button('I am just a gimmick button but lucas did not program me yet')

### top row 

st.markdown("## Main KPIs")
st.markdown(f"as of {totalvalue.index[-1]}")

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi = st.beta_columns(6)


with first_kpi:
    st.markdown("**Total Gain in AED**")
    number1 = round(totalvalue.iloc[-1,2],3)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Total Gain in %**")
    number2 = round(totalvalue.iloc[-1,4],3)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Daily Gain in AED**")
    number3 = round(totalvalue.iloc[-1,3],3)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number3}</h1>", unsafe_allow_html=True)
    
with fourth_kpi:
    st.markdown("**Daily Gain in %**")
    number4 = round(totalvalue.iloc[-1,5],3)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number4}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**Average productivity BTC p.d.**")
    number5 = round(kpis.iloc[-1,2],6)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number5}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown("**Daily productivity BTC p.d.**")
    number6 = round(kpis.iloc[-1,1],6)
    st.markdown(f"<h1 style='text-align: left; color: red;'>{number6}</h1>", unsafe_allow_html=True)

st.markdown("<hr/>", unsafe_allow_html=True)



st.markdown("## Total Gain and Total Value vs Invested")

first_chart, second_chart = st.beta_columns(2)

with first_chart:
    chart_data = totalvalue['%Total Gain']
    st.bar_chart(chart_data)

     
with second_chart:
    df = totalvalue
    df.reset_index(drop=True, inplace=True)
    chart_data = df[['Total Value', 'Total invested']]
    st.area_chart(chart_data)

    
    

st.markdown("<hr/>", unsafe_allow_html=True)


st.markdown("forecast yearly return")

st.line_chart(totalvalue[['% cummulating p.a.', '% average p.a.']])

st.markdown("<hr/>", unsafe_allow_html=True)

st.markdown("Total Value")
st.dataframe(totalvalue)
#st.table(totalvalue)

st.markdown("workingc apital")
st.dataframe(workingcapital)

st.markdown("static capital")
st.dataframe(staticcapital)



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
