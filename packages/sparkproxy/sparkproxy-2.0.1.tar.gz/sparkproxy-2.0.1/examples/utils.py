# -*- coding: utf-8 -*-
import random
import time
from datetime import datetime
import pytz

def generate_order_id():
    timestamp = int(time.time() * 1000)  # 毫秒级时间戳
    random_num = random.randint(1000, 9999)
    order_id = "{}{}".format(timestamp, random_num)
    return order_id


# Function to convert a timestamp to local time
def timestamp_to_local(timestamp, local_timezone="Asia/Shanghai"):
    # Convert the timestamp to a datetime object
    utc_time = datetime.utcfromtimestamp(timestamp)
    utc_time = utc_time.replace(tzinfo=pytz.utc)

    # Convert to the desired local timezone
    local_time = utc_time.astimezone(pytz.timezone(local_timezone))
    return local_time