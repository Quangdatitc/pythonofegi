#non_running_display.py

import datetime

def nonjobhour_display_msg():
    current_datetime = datetime.datetime.now()
    target_time = current_datetime.replace(hour=7, minute=50, second=0, microsecond=0) + datetime.timedelta(days=1)
    time_difference = target_time - current_datetime
    hours, remainder = divmod(time_difference.total_seconds(), 3600)
    minutes, sec = divmod(remainder, 60)
    display_msg = f"営業開始まで: {int(hours)} 時間 {int(minutes)} 分 {round(sec)} 秒　残り"
    return f"<h1 style='text-align: center;color: gray;font-size: 70px;margin-top: 30%;transform: translateY(-50%);'>{display_msg}</h1>"
