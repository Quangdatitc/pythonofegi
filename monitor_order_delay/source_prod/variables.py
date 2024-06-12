#variables.py

import pandas as pd
import datetime
 
 
times = [900, 1000, 1100, 1200,1400, 1500, 1600, 1700]

color_mapping = {
        "gray": "rgba(169, 169, 169, 1)",
        "red": "rgba(255, 0, 0, 1)",
        "yellow": "rgba(255, 255, 0, 0.75)",
        "blue": "rgba(61, 157, 253, 0.7)",
    }

start_time = 750
finish_time = 1730
blue_color = "rgba(169, 169, 169, 1)"
column_list = ["品目番号", "品目名称","納入時刻" ,"供給者", "使用者","Ｐ／Ｆ（送り先）"]
title = "日納入品の未受入確認監視モニター"

pathData = r"C:\Users\RP00056\monitor_order_delay\data\result.csv"

def load_custom_html_and_css():
    with open('custom.css', 'r', encoding='utf-8') as css_file:
        custom_css = css_file.read()
    return custom_css

current_moment = datetime.datetime.now().time().hour * 100 + datetime.datetime.now().time().minute

class Data:
    my_list_T = pd.DataFrame()
    my_list_D = pd.DataFrame()
    data_e = pd.DataFrame()
    data_c = pd.DataFrame()
    pathDataMorningFirst = r"C:\Users\RP00056\monitor_order_delay\data\result_" + datetime.date.today().strftime("%Y%m%d")+ '.csv'
    pathLogo = r'C:\Users\RP00056\monitor_order_delay\Log\streamline_log_' + datetime.date.today().strftime("%Y%m%d")+ '.log'
    current_moment = datetime.datetime.now().time().hour * 100 + datetime.datetime.now().time().minute
    @classmethod
    def initialize_variables(cls):
        cls.my_list_D = pd.DataFrame()
        cls.my_list_T = pd.DataFrame()
        cls.data_e = pd.DataFrame()
        cls.data_c = pd.DataFrame()
        cls.current_moment = datetime.datetime.now().time().hour * 100 + datetime.datetime.now().time().minute
        cls.pathDataMorningFirst = r"C:\Users\RP00056\monitor_order_delay\data\result_" + datetime.date.today().strftime("%Y%m%d")+ '.csv'
        cls.pathLogo = r'C:\Users\RP00056\monitor_order_delay\Log\streamline_log_' + datetime.date.today().strftime("%Y%m%d")+ '.log'
