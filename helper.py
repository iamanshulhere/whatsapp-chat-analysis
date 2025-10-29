from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter

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