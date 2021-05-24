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

totalvalue = pd.read_pickle(https://github.com/Mentalustig/Bitcoindashboard/blob/main/totalvalue.pkl)
workingcapital = pd.read_pickle(https://github.com/Mentalustig/Bitcoindashboard/blob/main/workingcapital.pkl)
totalvalue = pd.read_pickle(https://github.com/Mentalustig/Bitcoindashboard/blob/main/totalvalue.pkl)
kpis = pd.read_pickle(https://github.com/Mentalustig/Bitcoindashboard/blob/main/kpis.pkl)



st.set_page_config(page_title = 'Streamlit Dashboard', layout='wide', page_icon='💹')

### top row 

st.markdown("## Main KPIs")

first_kpi, second_kpi, third_kpi, fourth_kpi, fifth_kpi, sixth_kpi = st.beta_columns(6)


with first_kpi:
    st.markdown("**Total Gain in AED**")
    number1 = round(totalvalue.iloc[-1,2],3)
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number1}</h1>", unsafe_allow_html=True)

with second_kpi:
    st.markdown("**Total Gain in %**")
    number2 = round(totalvalue.iloc[-1,4],3)
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number2}</h1>", unsafe_allow_html=True)

with third_kpi:
    st.markdown("**Daily Gain in AED**")
    number3 = round(totalvalue.iloc[-1,3],3)
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number3}</h1>", unsafe_allow_html=True)
    
with fourth_kpi:
    st.markdown("**Daily Gain in %**")
    number4 = round(totalvalue.iloc[-1,5],3)
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number4}</h1>", unsafe_allow_html=True)

with fifth_kpi:
    st.markdown("**Average productivity BTC p.d.**")
    number5 = round(kpis.iloc[-1,2],6)
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number5}</h1>", unsafe_allow_html=True)

with sixth_kpi:
    st.markdown("**Daily productivity BTC p.d.**")
    number6 = round(kpis.iloc[-1,1],6)
    st.markdown(f"<h1 style='text-align: center; color: red;'>{number6}</h1>", unsafe_allow_html=True)


st.markdown("<hr/>", unsafe_allow_html=True)


st.markdown("## Total Gain and Total Value vs Invested")

first_chart, second_chart = st.beta_columns(2)


with first_chart:
    chart_data = totalvalue['%Total Gain']
    st.line_chart(chart_data)

with second_chart:
    chart_data = totalvalue[['Total Value', 'Total invested']]
    st.line_chart(chart_data)


st.markdown("<hr/>", unsafe_allow_html=True)


st.markdown("forecast yearly return")

st.line_chart(totalvalue[['% cummulating p.a.', '% average p.a.']])

    
