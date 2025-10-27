import pandas as pd
import re

def preprocess(data):
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?:\s?[apAP][mM])?'
    messages = re.split(pattern + r'\s-\s', data)[1:]
    messages = [m.lstrip('- ').strip() for m in messages]
    dates = re.findall(pattern, data)
    dates = [d.replace('\u202f', ' ') for d in dates]
    
    # Align dates and messages
    min_len = min(len(dates), len(messages))
    dates = dates[:min_len]
    messages = messages[:min_len]
    
    # Parse dates into datetime objects
    def parse_date(d):
        for fmt in ['%d/%m/%y, %I:%M %p', '%d/%m/%y, %H:%M']:
            try:
                return pd.to_datetime(d, format=fmt)
            except:
                continue
        return pd.NaT

    parsed_dates = [parse_date(d) for d in dates]
    df = pd.DataFrame({'user_message': messages, 'date': parsed_dates})
    
    # Split sender and message text
    users = []
    messages_list = []

    for message in df['user_message']:
        if ': ' in message:
            user, msg = message.split(': ', 1)
        else:
            user, msg = 'group_notification', message
        users.append(user)
        messages_list.append(msg)

    df['user'] = users
    df['messages'] = messages_list
    df.drop(columns=['user_message'], inplace=True)
    
    df['year'] = df['date'].dt.year
    
    df['month'] = df['date'].dt.month_name()
    
    df['day'] = df['date'].dt.day
    
    df['hour'] = df['date'].dt.hour
    
    df['minute'] = df['date'].dt.minute
    
    return df