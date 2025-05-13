from datetime import datetime as dt
import re

def auto_date_parse(date_string):
    """
    Takes in an html form date or dat-time string.
    Will determine if it includes a time alongisde the date and create a datetime object accordingly.
    If the time is not included it will default to 23:59 (11:59 PM) the date it is due.
    """    
    if type(date_string) is not str:
        raise ValueError("date_string is not of type str")
    
    date_string = date_string.strip()
    try:
        if re.search("T[0-2][0-9]:[0-5][0-9]", date_string) is None:
            date_string = date_string+" 23:59"
            return dt.strptime(date_string, "%Y-%m-%d %H:%M")
        else:
            return dt.strptime(date_string, "%Y-%m-%dT%H:%M")
    except ValueError:
        return None
