from urlextract import URLExtract
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
    x = df['user'].value_counts().head()
    
    return x