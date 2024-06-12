#main.py
import streamlit as st
import datetime
import time
import logging
 
from Logger import setup_logger
from run_batch import run_batch
from non_running_display import nonjobhour_display_msg
from leftPart import displayFlow
from get_data import get_display_prime_data
from variables import  start_time,title,finish_time,Data
from non_running_display import nonjobhour_display_msg
from run_batch import run_batch
current_time = datetime.datetime.now().time()
current_hour = current_time.hour * 100 + current_time.minute
 

st.set_option('deprecation.showfileUploaderEncoding', False)
st.set_page_config(page_icon="🧊",layout="wide",page_title=title)

def main():
    try:

        setup_logger()
        content = st.empty()
        batch_executed = False
        rerun_flag = True
        
        while True:
            if datetime.datetime.now().weekday() == 6:
                nonjobhour_display_msg()
                time.sleep(300)
            else:    
                # Data.initialize_variables()
                current_time = datetime.datetime.now().time() 
                current_hour = current_time.hour * 100 + current_time.minute
                content.empty()
    
                if start_time   <= current_hour < finish_time :
                    Data.initialize_variables()
                    if current_hour % 10 == 0 and not batch_executed:
                        run_batch()
                        batch_executed = True
                        rerun_flag = True
                    elif current_hour % 10 != 0:
                        batch_executed = False

                    get_display_prime_data(True)
                    get_display_prime_data(False)
                    displayFlow()
                    st.rerun()
                    if current_hour % 10 == 0 and rerun_flag:
                        st.rerun()
                        rerun_flag = False

                else:
                    content.markdown(nonjobhour_display_msg(),unsafe_allow_html=True)
                    time.sleep(10)
            time.sleep(10)

    except Exception as e:
        logging.error(f"An error occured: {str(e)}")

if __name__ == "__main__":
    main()