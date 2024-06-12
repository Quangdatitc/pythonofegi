#run_batch.py
import streamlit as st
import time
import subprocess
import logging

logger = logging.getLogger(__name__)

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
        logging.info("vbs script 開始開始")
        vbs_process = subprocess.Popen(['cscript.exe',vbs_script_path],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        vbs_stdout, vbs_stderr = vbs_process.communicate()
        count = 0
        while count < 180:
            if vbs_process.returncode == 0:
                break
            count += 1
            time.sleep(1)    
            
        # time.sleep(60)
        logging.info("batch file 実行開始：")
        completed_process = subprocess.run(
                batch_file_path, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=False
            )
    if completed_process.returncode != 0:
        stderr = completed_process.stderr.decode('utf-8', 'ignore')  # Decode stderr as UTF-8
        logging.info("batch file 実行エラー：")
        logging.info(stderr)
        return False
    else:
        stdout = completed_process.stdout.decode('utf-8', 'ignore')  # Decode stdout as UTF-8
        logging.info("batch file 実行成功")
        return True

def display_spin():
    return """
            <style>
            .stSpinner { display: flex; justify-content: center; align-items: center; }
            .stSpinner div { width: 400px; height: 400px; }
            </style>
            """