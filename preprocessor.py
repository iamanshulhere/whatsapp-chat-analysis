import pandas as pd
import re
from dateutil import parser

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

    # Parse dates safely (supports MM/DD and DD/MM automatically)
    def parse_date(d):
        try:
            return parser.parse(d)
        except:
            return pd.NaT

    df = pd.DataFrame({'user_message': messages, 'date': dates})
    df['date'] = df['date'].apply(parse_date)

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

    # dt extractions (only if date is parsed correctly)
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    # Create time period slot
    period = []
    for hour in df['hour'].fillna(0).astype(int):
        if hour == 23:
            period.append(f"{hour}-00")
        elif hour == 0:
            period.append("00-1")
        else:
            period.append(f"{hour}-{hour+1}")
    df['period'] = period

    return df
