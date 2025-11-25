import pandas as pd
import re
from dateutil import parser
import pdfplumber

def extract_pdf_text(file_bytes):
    text = ""
    with pdfplumber.open(file_bytes) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def preprocess(data, is_pdf=False):

    
    if is_pdf:
        data = extract_pdf_text(data)
    
    # Clean text for PDF wraps
    data = data.replace("\n", " ")
    data = re.sub(r"\s+", " ", data)

    # Flexible date matching
    pattern = r'\d{1,2}/\d{1,2}/\d{2,4},\s*\d{1,2}:\d{2}(?:\s?[APMapm]{2})?'

    dates = re.findall(pattern, data)
    messages = re.split(pattern + r'\s-\s', data)[1:]

    # Align
    min_len = min(len(dates), len(messages))
    dates = dates[:min_len]
    messages = messages[:min_len]

    # Date parsing
    def parse_date(d):
        try:
            return parser.parse(d, dayfirst=True)
        except:
            return pd.NaT

    df = pd.DataFrame({"user_message": messages, "date": dates})
    df["date"] = df["date"].apply(parse_date)

    # USER + MESSAGE SPLIT
    users = []
    msg_list = []
    for m in df["user_message"]:
        if ": " in m:
            u, t = m.split(": ", 1)
        else:
            u, t = "group_notification", m
        users.append(u)
        msg_list.append(t)

    df["user"] = users
    df["messages"] = msg_list
    df.drop(columns=["user_message"], inplace=True)

    # DATETIME FIELDS
    df["only_date"] = df["date"].dt.date
    df["year"] = df["date"].dt.year
    df["month_num"] = df["date"].dt.month
    df["month"] = df["date"].dt.month_name()
    df["day"] = df["date"].dt.day
    df["day_name"] = df["date"].dt.day_name()
    df["hour"] = df["date"].dt.hour
    df["minute"] = df["date"].dt.minute

    # PERIOD
    df["period"] = df["hour"].fillna(0).astype(int).apply(
        lambda h: f"{h}-{0}" if h == 23 else ("00-1" if h == 0 else f"{h}-{h+1}")
    )

    return df
