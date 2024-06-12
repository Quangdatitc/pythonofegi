#get_data.py

import pandas as pd
from variables import pathData,Data

def get_display_prime_data(is_current_data):
    if is_current_data:
        data = pd.read_csv(pathData,encoding='shift_jis')
        Data.data_c = {
            'T2': data[data['type'] == "T2"],
            'T4': data[data['type'] == "T4"],
            'D': data[data['type'] == "D"],
            'Tother':data[data['type'] == "T"]
        }
    else:
        data = pd.read_csv(Data.pathDataMorningFirst,encoding='shift_jis')
        Data.data_e = {
            'T2': data[data['type'] == "T2"],
            'T4': data[data['type'] == "T4"],
            'D': data[data['type'] == "D"],
            'Tother':data[data['type'] == "T"]
        }