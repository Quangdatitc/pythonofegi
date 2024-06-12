#leftPart.py

import streamlit as st
from header import hide_header
from variables import load_custom_html_and_css
from display_one_block import display_one_block
from variables import color_mapping,times,column_list,Data
import pandas as pd
import datetime
import time
from displayLateOrderLists import displayLateOrders
 

def displayFlow():
 
    new_container = st.empty()
    hide_header()
    
    custom_css = load_custom_html_and_css()
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    
    with new_container.container():
        timer, t_flow, d_flow, kanban = st.columns([1,1,1,3])
        with timer:
                st.markdown(display_one_block(color_mapping["blue"],"残数/計画数"),unsafe_allow_html=True)
                create_time_block_section("Time")
        with t_flow:
                st.markdown(display_one_block(color_mapping["blue"],"Tオーダー"),unsafe_allow_html=True)
                create_time_block_section("T")
        with d_flow:
                st.markdown(display_one_block(color_mapping["blue"],"Dオーダー"),unsafe_allow_html=True)
                create_time_block_section("D")
        with kanban:    
            displayLateOrders()
 
        time.sleep(40)

def create_time_block_section(flow):
    if flow == "T":
        for time in times:
            st.markdown(display_time_block(time,flow), unsafe_allow_html=True)
    else:
        for time in times:
            st.markdown(display_time_block(time,flow), unsafe_allow_html=True)

 
def display_time_block(time,flow):
    if flow =="Time":
        if time != 900: 
            time_str = str(time//100) + ":00"
        else: 
            time_str = "0" + str(time//100) + ":00"

        if Data.current_moment > time:
            return display_one_block(color_mapping["gray"],time_str)
        else:
            return display_one_block(color_mapping["blue"],time_str)
   
    if time == 1700:
        bunshi,bunbo =  len(pd.concat([Data.data_c['T2'],Data.data_c['T4'],Data.data_c['Tother']]).reset_index(drop=True)),len(Data.data_e['T4']) + len(Data.data_e['T2'])  + len(Data.data_e['Tother'])      
        #      #T
        bunshi_d, bunbo_d = len(Data.data_c['D']), len(Data.data_e['D'] == time)                                                                                        #D
 
    else:
        bunshi = (Data.data_c['T2']['納入時刻'] == time).sum() + (Data.data_c['T4']['納入時刻'] == time).sum() + (Data.data_c['Tother']['納入時刻'] == time).sum()                          #T
        bunbo = (Data.data_e['T2']['納入時刻'] == time).sum() + (Data.data_e['T4']['納入時刻'] == time).sum() + (Data.data_e['Tother']['納入時刻'] == time).sum()   #D
        bunshi_d, bunbo_d = (Data.data_c['D']['納入時刻'] == time).sum(),  (Data.data_e['D']['納入時刻'] == time).sum()

    bg = get_block_color(int(time),flow)

    return display_one_block(bg,"{} / {}".format(bunshi_d,bunbo_d)) if flow == "D" else display_one_block(bg,"{} / {}".format(bunshi,bunbo))


def get_block_color(time,flow):
    
    if Data.current_moment < (time - 50):
        return color_mapping["blue"]#計画
    
    if flow == "T":
 
        t2_has_data = (Data.data_c['T2']['納入時刻'] == time).sum() > 0
        t4_has_data = (Data.data_c['T4']['納入時刻'] == time).sum() > 0
        tother_has_data = (Data.data_c['Tother']['納入時刻'] == time).sum() > 0

        if not any([t2_has_data,t4_has_data,tother_has_data]):
            return color_mapping["gray"]
        if tother_has_data: 
            Data.my_list_T = add_delayed_order_to_list(Data.my_list_T,Data.data_c['Tother'],time)
        if t2_has_data: 
            Data.my_list_T = add_delayed_order_to_list(Data.my_list_T,Data.data_c['T2'],time)
        if t4_has_data:  
            Data.my_list_T = add_delayed_order_to_list(Data.my_list_T,Data.data_c['T4'],time)

        return color_mapping["red"]

    else:
        d_has_data =  (Data.data_c['D']['納入時刻'] == time).sum() > 0

        if not d_has_data:
            return color_mapping["gray"]
        if d_has_data: 
            Data.my_list_D = add_delayed_order_to_list(Data.my_list_D,Data.data_c['D'],time)
        return color_mapping["yellow"]

def add_delayed_order_to_list(order_list,data,hour):
    filtered_data = data[data['納入時刻'] == hour][column_list]
    return  pd.concat([order_list, filtered_data], ignore_index=True).reset_index(drop=True)
 