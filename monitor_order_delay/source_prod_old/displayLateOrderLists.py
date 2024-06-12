#displayLateOrderLists.py
import streamlit as st
import pandas as pd
from variables import Data
 
def displayLateOrders():
    if len(Data.my_list_D) == 0 and len(Data.my_list_T) == 0:
        st.markdown(
            f"""
            <div style="text-align:center;font-size:2vw;color:black; background-color:white; flex: 1; width: 15em;max-width: 80em; height: auto; max-height: 74vh; overflow-y: auto;overflow-x: auto;margin-left:2em; margin-top:40%;padding-top:2.5vh;padding-bottom:2.5vh;">
                遅延無し
            </div>
            """,
            unsafe_allow_html=True
        )
        return
        
        
    if len(Data.my_list_T) > 0:
        res_T = convert_data_to_display(Data.my_list_T)  
        
    if len(Data.my_list_D) > 0:
        res = convert_data_to_display(Data.my_list_D)


    if len(Data.my_list_T) > 0 and len(Data.my_list_D) > 0:
        data = pd.concat([res_T,res],ignore_index=True)
        order_type = [len(Data.my_list_T),len(Data.my_list_D)]
    elif len(Data.my_list_D) > 0:
        data = res
        order_type = "D"
    elif len(Data.my_list_T) > 0:
        data = res_T
        order_type = "T"

    st.markdown(color_text(order_type), unsafe_allow_html=True)
    return st.markdown(
        
            f"""
            <div style="flex: 1; width: auto;max-width: 95em; height: auto; max-height: 85vh; overflow-y: auto;overflow-x: auto;margin-left:5%;">
                {data.to_html(escape=False)}
            </div>
            """,
            unsafe_allow_html=True
        )


def convert_data_to_display(delay_order):
    headers = ["品目番号<br>品目名称", "納入時刻" ,"供給者<br>使用者", "Ｐ／Ｆ（送り先）"]
    data = delay_order
    data['使用者'] = data['使用者'].apply(lambda x: str(x))
    data['供給者'] = data['供給者'].apply(lambda x: str(x))
    data['品目番号'] = data['品目番号'] + '<br>' + data['品目名称']
    data['供給者'] = data['供給者'] + '<br>' + data['使用者']
 
    result = data.drop(columns=['使用者', '品目名称']).rename(columns={'品目番号': '品目番号<br>品目名称'})
    result.columns = headers
    result.sort_values(by='納入時刻', ascending=False,inplace=True)
    result['納入時刻'] = result['納入時刻'].apply(lambda x = 900: str(x))
    result['納入時刻'][result['納入時刻'] == "900"] = "0900"
    blankIndex = ['']*len(result)
    result.index = blankIndex
    return result

def color_text(props=None):
         
        common_style = """
            th {
                border: 0.2vw solid black;
                text-align: center;
                background-color: white;
                color: black;
                font-size: 1.5vw;
                white-space: nowrap;
            }
            th:first-child {
                display: none;
            }

            .dataframe tbody tr {
                border: 0.2vw solid black;
                background-color: white; 
                text-align: center;
                font-size: 1.5vw;
            }
        """
 
        if isinstance(props,list):
            T = props[0]
            D = props[1]
            return f"""
                <style>
                    {common_style}
                    .dataframe tbody tr:nth-child(n+{T+1}):nth-child(-n+{T+ D}) {{ color: orange;}}
                    .dataframe tbody tr:nth-child(n+1):nth-child(-n+{T}) {{ color: red; }}
                </style>
                """

        if props == "T":
            return f"""
                    <style>
                        {common_style}
                        .dataframe tbody tr {{color:red;}}
                    </style>
                """
        elif props == "D":
            return f"""
                    <style>
                        {common_style}
                        .dataframe tbody tr {{color:orange;}}
                    </style>
                """

        
