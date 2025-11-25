from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords


extractor = URLExtract()
def fetch_stats(selected_user, df):
    
    # Filter if a specific user is selected
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # 1. Fetch number of messages
    num_messages = df.shape[0]
    
    # 2. Count number of words
    words = []
    for message in df['messages']:
        words.extend(message.split())
        
    
    # fetch the number of media messages
    num_media = df[df['messages'] == '<Media omitted>'].shape[0]
    
    # fetch the number of links
    
    links = []
    for link in df['messages']:
        links.extend(extractor.find_urls(message))
    
    return num_messages, len(words), num_media, len(links)



# Function for find the most Busy person

def most_busy_users(df):
    
    # Remove 'group_notification' entries
    temp = df[df['user'] != 'group_notification']
    
    x = temp['user'].value_counts().head()
    
    # Calculating percentage 
    percentage_df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index()
    percentage_df.columns = ['name', 'percent']
    
    return x, percentage_df


def create_wordcloud(selected_user, df):
    
    # Filter if a specific user is selected
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    wc = WordCloud(width = 500, height = 500, min_font_size = 18, background_color = 'white')
    
    df_wc = wc.generate(df['messages'].str.cat(sep = " "))
    
    return df_wc

def most_common_words(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['messages'] != '<Media omitted>']
    
    stop_words = set(stopwords.words('english'))
    
    words = []
    for message in temp['messages']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
            
    most_common__df = pd.DataFrame(Counter(words).most_common(25))
    
    return most_common__df


def emoji_helper(selected_user, df):
    
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if emoji.is_emoji(c)])
        
    emoji_df = pd.DataFrame(Counter(emojis).most_common(), columns=['Emoji', 'Count'])
    
    return emoji_df


def monthly_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    time_line = df.groupby(['year', 'month_num', 'month']).count()['messages'].reset_index()
    
    time = []
    
    for i in range(time_line.shape[0]):
        time.append(time_line['month'][i] + "-" + str(time_line['year'][i]))
        
    time_line['time'] = time
        
    return time_line


def daily_timeline(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    daily_timeline = df.groupby('only_date').count()['messages'].reset_index()
    
    return daily_timeline
    
    
    
def week_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # correct order of days
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    busy_day = df['day_name'].value_counts()
    busy_day = busy_day.reindex(order).fillna(0)  # arranges in correct order
    
    return busy_day
    
    
def month_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # correct order of months
    order = ["January", "February", "March", "April", "May", "June",
             "July", "August", "September", "October", "November", "December"]

    busy_month = df['month'].value_counts()
    busy_month = busy_month.reindex(order).fillna(0)

    return busy_month




def activity_heatmap(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Correct day order
    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # Use ONLY periods that actually appear in the chat
    period_order = sorted(df['period'].unique(), key=lambda x: int(x.split('-')[0]) )

    heatmap_df = df.pivot_table(
        index='day_name',
        columns='period',
        values='messages',
        aggfunc='count'
    ).fillna(0)

    heatmap_df = heatmap_df.reindex(day_order)
    heatmap_df = heatmap_df.reindex(columns=period_order)

    return heatmap_df


