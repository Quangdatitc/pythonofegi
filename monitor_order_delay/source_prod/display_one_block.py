#one_block_display.py
# def display_one_block(skin_color,number):
# ローカル
#     return f"""
#     <div style="display: flex; justify-content: space-between; align-items: center;">
#         <div style='background-color: {skin_color}; flex:1; width: auto; max-width:20em; height: auto;max-height:8vh;padding: 1px 1px ; margin: 10px 10px 0.5vw 0px; border-radius: 5px; text-align: center;overflow-y: auto;overflow-x: auto;'>
#             <span style='color: rgb(0, 0, 0); font-size: 2vw;'>
#                 <b>{number}</b>
#             </span>
#         </div>
#     </div>
#                 """

# 工務室
def display_one_block(skin_color,number):
    
    return f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style='background-color: {skin_color}; flex:1; width: 80%; max-width:35em; height: auto; 
        max-height:35vh; padding: 3% 1%; margin: 0 1.1% 1vw 1vw; border-radius: 1%; text-align: center; overflow-y: auto; overflow-x: auto;'>
            <span style='color: rgb(0, 0, 0); font-size: 2vw;'>
                <b>{number}</b>
            </span>
        </div>
    </div>
    """