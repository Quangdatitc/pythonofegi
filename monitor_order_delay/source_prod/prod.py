from tkinter import NO
import streamlit as st
import pandas as pd
import datetime
import time
import subprocess
import shutil
import logging
import os
state = st.session_state
  
st.set_page_config(page_icon="🧊",layout="wide",page_title="日納入品の未受入確認監視モニター")
@st.cache_data(ttl=60)

def display_spin():
    return """
                <style>
                .stSpinner { display: flex; justify-content: center; align-items: center; }
                .stSpinner div { width: 400px; height: 400px; }
                </style>
                """

def display_block_html(skin_color,number):
    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style='background-color: {skin_color}; flex:1; width: auto; max-width:20em; height: auto;max-height:8vh;padding: 1px 1px ; margin: 10px 10px 0.5vw 0px; border-radius: 5px; text-align: center;overflow-y: auto;overflow-x: auto;'>
            <span style='color: rgb(0, 0, 0); font-size: 2vw;'>
                <b>{number}</b>
            </span>
        </div>
    </div>
                """

def get_unique_key():
    return f"custom-text-area-{time.time()}"

def run_batch():

    vbs_script_path = r"C:\Users\RP00056\monitor_order_delay\未受入未検収進捗.vbs"
    batch_file_path = r"C:\Users\RP00056\monitor_order_delay\main.bat"
    with st.spinner("データを取得中 ..."):
        st.markdown(
                """
                <style>
                .stSpinner { display: flex; justify-content: center; align-items: center; }
                .stSpinner div { width: 400px; height: 400px; }
                </style>
                """,
                unsafe_allow_html=True,
            )
        vbs_process = subprocess.Popen(['cscript.exe',vbs_script_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        vbs_stdout, vbs_stderr = vbs_process.communicate()
        count = 0
        while count < 180:
            if vbs_process.returncode == 0:
                break
            count += 1
            time.sleep(1)    
            
        # time.sleep(60)
        completed_process = subprocess.run(
                batch_file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False
            )
    if completed_process.returncode != 0:
        stderr = completed_process.stderr.decode('utf-8', 'ignore')  # Decode stderr as UTF-8
        logging.info("Error during batch file execution:")
        logging.info(stderr)
        return False
    else:
        stdout = completed_process.stdout.decode('utf-8', 'ignore')  # Decode stdout as UTF-8
        logging.info("Batch file executed successfully:")
        # print(stdout)
        logging.info(stdout)
        return True

        
def add_delayed_order_to_list(order_list,data,hour):
    filtered_data = data[data['納入時刻'] == hour][["品目番号", "品目名称","納入時刻" ,"供給者", "使用者","Ｐ／Ｆ（送り先）"]]
    return  pd.concat([order_list, filtered_data], ignore_index=True)

def load_custom_html_and_css():
    with open('template\custom.html', 'r', encoding='utf-8') as html_file:
        custom_html = html_file.read()
    with open('template\custom.css', 'r', encoding='utf-8') as css_file:
        custom_css = css_file.read()
    return custom_html, custom_css

def format_user(row):
                return f"{row['供給者']}\n{row['使用者']}"
def displayFlow(data,data_prime,content):

    new_container = st.empty()
    st.markdown(hide_streamlit_style,unsafe_allow_html=True) 
    custom_html, custom_css = load_custom_html_and_css()
    st.markdown(f'<style>{custom_css}</style>', unsafe_allow_html=True)
    
    with new_container.container():
        timer, t_flow, d_flow, kanban = st.columns([1,1,1,3])
        with timer:
                st.markdown(display_block_html("rgba(61, 157, 253, 0.7)","残数/計画数"),unsafe_allow_html=True)
                create_time_block_section( "", data['T2'], data['T4'], data['D'],data['Tother'],data_prime,"Time")
        with t_flow:
                st.markdown(display_block_html("rgba(61, 157, 253, 0.7)","Tオーダー"),unsafe_allow_html=True)
                create_time_block_section( "", data['T2'], data['T4'], data['D'],data['Tother'],data_prime,"T")
        with d_flow:
                st.markdown(display_block_html("rgba(61, 157, 253, 0.7)","Dオーダー"),unsafe_allow_html=True)
                create_time_block_section( "", data['T2'], data['T4'], data['D'],data['Tother'],data_prime,"D")
        with kanban:   
            if len(my_list_D) == 0 and len(my_list_T) == 0:
                st.markdown(
                    f"""
                    <div style="text-align:center;font-size:2vw;color:black; background-color:white; flex: 1; width: 15em;max-width: 80em; height: auto; max-height: 74vh; overflow-y: auto;overflow-x: auto;margin-left:2em; margin-top:40%;padding-top:2.5vh;padding-bottom:2.5vh;">
                        遅延無し
                    </div>
                    """,
                    unsafe_allow_html=True
                ) 
        
            if len(my_list_T) > 0:
                res_T = cake(my_list_T)  
                
            if len(my_list_D) > 0:
                res = cake(my_list_D)

            if len(my_list_T) > 0 and len(my_list_D) > 0:
                combined = pd.concat([res,res_T])
                st.markdown(color_text("TD",len(my_list_T),len(my_list_D)), unsafe_allow_html=True)
                
                # st.markdown(f'<div style="flex:1; width:700px; height:30rem;">{combined.head(9).to_html(escape=False)}</div>', unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style="flex: 1; width: auto;max-width: 80em; height: auto; max-height: 74vh; overflow-y: auto;overflow-x: auto;margin-left:2em;">
                        {combined.to_html(escape=False)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
  
            elif len(my_list_D) > 0:
                st.markdown(color_text("D"), unsafe_allow_html=True)
                # st.markdown(f'<div style="flex:1; width:700px; height:100%;">{res.head(30).to_html(escape=False)}</div>', unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style="flex: 1; width: auto;max-width: 80em; height: auto; max-height: 74vh; overflow-y: auto;overflow-x: auto;margin-left:2em;">
                        {res.to_html(escape=False)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            elif len(my_list_T) > 0:
                st.markdown(color_text("T"), unsafe_allow_html=True)
                # st.markdown(f'<div style="flex:1; width:700px; height:100%;">{res_T.head(9).to_html(escape=False)}</div>', unsafe_allow_html=True)
                st.markdown(
                    f"""
                    <div style="flex: 1; width: auto;max-width: 80em; height: auto; max-height: 74vh; overflow-y: auto;overflow-x: auto;margin-left:2em;">
                        {res_T.to_html(escape=False)}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        time.sleep(40)

def cake(delay_order):
    delay_order['使用者'] = delay_order['使用者'].apply(lambda x: str(x))
    delay_order['品目番号'] = delay_order['品目番号'] + '<br>' + delay_order['品目名称']
    delay_order['供給者'] = delay_order['使用者'] + '<br>' + delay_order['使用者']
    headers = ["品目番号<br>品目名称", "納入時刻" ,"供給者<br>使用者", "Ｐ／Ｆ（送り先）"]
    result = delay_order.drop(columns=['使用者']).drop(columns=['品目名称'])
    result.columns = headers
    result.sort_values(by='納入時刻', ascending=False, inplace=True)
    blankIndex = ['']*len(result)
    result.index = blankIndex
    return result

def color_text(prop,T=None,D=None):
        common_style = """
            th {
                border: 3px solid black;
                text-align: center;
                background-color: white;
                color:black;
                font-size: 1.25vw;
                white-space: nowrap;
            }

            th:first-child{
                display:none;
            }
            
            .dataframe tbody tr {
                border: 3px solid black;
                background-color: white; 
                text-align: center;
                font-size: 1.25vw;
 
                
            }

        """

        if prop == "T":
            return """
                    <style>
                        {common_style}
                        .dataframe tbody tr {{color:red;}}
                    </style>
                """
        elif prop == "D":
            return f"""
                    <style>
                        {common_style}
                        .dataframe tbody tr {{color:orange;}}
                    </style>
                """

        elif prop == "TD":
            return f"""
                <style>
                    {common_style}
                    .dataframe tbody tr:nth-child(n+{T+1}):nth-child(-n+{T+D}) {{ color: orange;}}
                    .dataframe tbody tr:nth-child(n+1):nth-child(-n+{T}) {{ color: red; }}
                </style>
                """


def display_time_block(time, T2_order, T4_order, D_order,Tother_order,data_prime,flow):
    if flow =="Time":
        time_str = str(time//100) + ":00"
        if time < datetime.datetime.now().hour*100:
            return display_block_html(color_mapping["gray"],time_str)
        else:
            return display_block_html(color_mapping["blue"],time_str)
   
    
    if time == 1700:
        bunshi,bunbo =  len(pd.concat([T2_order,T4_order,Tother_order])),len(data_prime['T4']) + len(data_prime['T2'])  + len(data_prime['Tother'])           #T
        bunshi_d, bunbo_d = len(D_order), len(data_prime['D'] == time)                                                                                        #D
 
    else:
        bunshi = (T2_order['納入時刻'] == time).sum() + (T4_order['納入時刻'] == time).sum() + (Tother_order['納入時刻'] == time).sum()                          #T
        bunbo = (data_prime['T2']['納入時刻'] == time).sum() + (data_prime['T4']['納入時刻'] == time).sum() + (data_prime['Tother']['納入時刻'] == time).sum()   #D
        bunshi_d, bunbo_d = (D_order['納入時刻'] == time).sum(),  (data_prime['D']['納入時刻'] == time).sum()
         
    bg = get_block_color(T2_order, T4_order, Tother_order, D_order, current_hour, int(time),flow)

    return display_block_html(bg,"{} / {}".format(bunshi_d,bunbo_d)) if flow == "D" else display_block_html(bg,"{} / {}".format(bunshi,bunbo))

def get_block_color(T2_order, T4_order, Tother_order, D_order, current_hour, time,flow):
    
    if current_hour < (time - 50):
        return color_mapping["blue"]#計画
    
    if flow == "T":
        global my_list_T
        t2_has_data = (T2_order['納入時刻'] == time).sum() > 0
        t4_has_data = (T4_order['納入時刻'] == time).sum() > 0
        tother_has_data = (Tother_order['納入時刻'] == time).sum() > 0

        if not any([t2_has_data,t4_has_data,tother_has_data]):
            return color_mapping["gray"]
        if tother_has_data: 
            my_list_T = add_delayed_order_to_list(my_list_T,Tother_order,time)
        if t2_has_data: 
            my_list_T = add_delayed_order_to_list(my_list_T,T2_order,time)
        if t4_has_data:  
            my_list_T = add_delayed_order_to_list(my_list_T,T4_order,time)

        return color_mapping["red"]

    else:
        global my_list_D
        d_has_data =  (D_order['納入時刻'] == time).sum() > 0

        if not d_has_data:
            return color_mapping["gray"]
        if d_has_data: 
            my_list_D = add_delayed_order_to_list(my_list_D,D_order,time)
        return color_mapping["yellow"]

def create_time_block_section(title, T2_order, T4_order, D_order,Tother_order,data_prime,flow):
    st.write(title)
    times = [900, 1000, 1100, 1200,1400, 1500, 1600, 1700]
    if flow == "T":
        for time in times:
            st.markdown(display_time_block(time, T2_order, T4_order, D_order,Tother_order,data_prime,flow), unsafe_allow_html=True)
    else:
        for time in times:
            st.markdown(display_time_block(time, T2_order, T4_order, D_order,Tother_order,data_prime,flow), unsafe_allow_html=True)

def delete_todays_data():
    inputPath =  r"C:\Users\RP00056\monitor_order_delay\data\result.csv"
    if os.path.exists(inputPath):
        os.remove(inputPath)
def main():
    content = st.empty()
    start_time = 730
    finish_time = 1730
    rerun_flag = True
    batch_executed = False
    #ログ 
    # Configure the logging settings
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

    # Create a FileHandler to log messages to a specific file
    log_file = 'Log\streamline_log_' + datetime.date.today().strftime("%Y%m%d")+ '.log'  # Set the desired file name and path
    file_handler = logging.FileHandler(log_file)

    # Optionally, you can set the log level for the file handler (e.g., INFO, DEBUG)
    file_handler.setLevel(logging.INFO)

    # Create a formatter for the file handler
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Attach the file handler to the root logger
    logging.getLogger().addHandler(file_handler)
    logging.info("Streamlit started")
    flag_deleted = False
    executed_time = datetime.datetime.now().time()
    while True:
        if datetime.datetime.now().weekday() == 6:
            #sunday == 6
            content.markdown(nonjobhour_display_msg(),unsafe_allow_html=True)
            time.sleep(300)
        else:
            current_time = datetime.datetime.now().time() 
            current_hour = current_time.hour * 100 + current_time.minute
            content.empty()

            if start_time  <= current_hour < finish_time:
                if current_hour % 10 == 0 and not batch_executed:
                    logging.info(current_hour)
                    run_batch()
                    executed_time = datetime.datetime.now().time()
                    rerun_flag = True
                    batch_executed = True
                elif current_hour % 10 != 0:
                    batch_executed = False
                data_frames,data_frames_prime = get_display_prime_data(True),get_display_prime_data(False)
                displayFlow(data_frames,data_frames_prime,content)
                st.rerun()
                if current_hour % 10 == 0 and rerun_flag:
                    st.rerun()
                    rerun_flag = False

            elif 1740 <= current_hour <= 1740 and not flag_deleted:
                delete_todays_data()
                flag_deleted = True
                time.sleep(10)
            else:
                content.markdown(nonjobhour_display_msg(),unsafe_allow_html=True)
                time.sleep(2)
        time.sleep(10)
       
def get_csv_filename(todays_data):
    if todays_data:
        path = r"C:\Users\RP00056\monitor_order_delay\data\result_"
        current_date = datetime.date.today().strftime("%Y%m%d")
        return f"{path}{current_date}.csv"
    else:
        return  r"C:\Users\RP00056\monitor_order_delay\data\result.csv"

 
def csv_file_exists(todays_data):
    if todays_data:
        return os.path.isfile(get_csv_filename(True))
    else:
        return os.path.isfile(get_csv_filename(False))

def load_initial_data():
    if csv_file_exists(True):
        filename = get_csv_filename(True)
        df = pd.read_csv(filename, encoding='shift_jis')
        return df
    # if csv_file_exists(False) and datetime.datetime.now().hour == 8:
    if csv_file_exists(False):
        filename = get_csv_filename(False)
        file_destination = get_csv_filename(True)
        shutil.copy(filename, file_destination)
        return load_initial_data()

def get_display_prime_data(current_data):
    if current_data:
        inputPath =  r"C:\Users\RP00056\monitor_order_delay\data\result.csv"
        data = pd.read_csv(inputPath,encoding='shift_jis')
    else:
        data = load_initial_data()

    return {
        'T2': data[data['type'] == "T2"],
        'T4': data[data['type'] == "T4"],
        'D': data[data['type'] == "D"],
        'Tother':data[data['type'] == "T"]
    }

def nonjobhour_display_msg():
    current_datetime = datetime.datetime.now()
    target_time = current_datetime.replace(hour=7, minute=30, second=0, microsecond=0) + datetime.timedelta(days=1)
    time_difference = target_time - current_datetime
    hours, remainder = divmod(time_difference.total_seconds(), 3600)
    minutes, sec = divmod(remainder, 60)
    display_msg = f"営業開始まで: {int(hours)} 時間 {int(minutes)} 分 {round(sec)} 秒　残り"
    return f"<h1 style='text-align: center;color: gray;font-size: 70px;margin-top: 30%;transform: translateY(-50%);'>{display_msg}</h1>"

my_list_T = pd.DataFrame()
my_list_D = pd.DataFrame()   
color_mapping = {
        "gray": "rgba(192, 192, 192, 1)",
        "red": "rgba(255, 0, 0, 1)",
        "yellow": "rgba(255, 255, 0, 0.75)",
        "blue": "rgba(61, 157, 253, 0.7)"
    }
hide_streamlit_style = """
            <style> 
            .stDeployButton {visibility:hidden;}
            .st-emotion-cache-4z1n4l {display:none;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
current_time = datetime.datetime.now().time()
current_hour = current_time.hour * 100 + current_time.minute


if __name__ == "__main__":
    main()
