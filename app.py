import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

import matplotlib.font_manager as fm
plt.rcParams['font.family'] = ['Segoe UI Emoji']


st.sidebar.title("What'sapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    
try:
    data = bytes_data.decode("utf-8")
except:
    data = bytes_data.decode("latin-1", errors="ignore")

    df = preprocessor.preprocess(data)
    
    st.dataframe(df)
    
    
    # Fetch unique user
    
    user_list = df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    
    selected_user = st.sidebar.selectbox("Show analysis wrt", user_list)
    
    
    # Showing Stats from the chat
    if st.sidebar.button("Show Analysis"):
        
        num_messages, words, num_media, links = helper.fetch_stats(selected_user, df)
        
        
        st.title("Top Statistics")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
    
        with col2:
            st.header("Total Words")
            st.title(words)
            
        with col3:
            st.header("Media Shared")
            st.title(num_media)
            
        with col4:
            st.header("Total Links")
            st.title(links)
            
            
        # Monthly Timeline
        st.title("Monthly TimeLine")
        time_line = helper.monthly_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 4))
        
        ax.plot(time_line['time'], time_line['messages'], color = 'green')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
            
        # Daily Timeline
        
        st.title("Daily TimeLine")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, ax = plt.subplots(figsize=(12, 4))
        
        ax.plot(daily_timeline['only_date'], daily_timeline['messages'], color = 'darkblue')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        
        # Activity Map
        
        st.title("Activity Map")
        col1, col2 = st.columns(2)
        
        with col1:
            st.header("Most Busy Day")
            busy_day = helper.week_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_day.index, busy_day.values, color = 'purple')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
            
            
        with col2:
            st.header("Most Busy Mobth")
            busy_month = helper.month_activity_map(selected_user, df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values, color = 'maroon')
            plt.xticks(rotation = 'vertical')
            st.pyplot(fig)
        
        
        
        st.title("Weekly Activity Map")

        heatmap_df = helper.activity_heatmap(selected_user, df)

        fig, ax = plt.subplots(figsize=(16, 6))

        sns.heatmap(
            heatmap_df,
            cmap="YlOrRd",          # Bright, readable colors
            linewidths=0.4,
            linecolor="gray",
            square=True,            # perfect clean blocks
            cbar_kws={"shrink": 0.7}
        )

        plt.xticks(rotation=45)
        plt.xlabel("Time Period")
        plt.ylabel("Day of Week")

        st.pyplot(fig)


    
        # Finding busiest person in group
        
        if selected_user == 'Overall':
            st.title('Busy Users')
            x, new_df = helper.most_busy_users(df)
            fig, axis = plt.subplots()
            
            col1, col2 = st.columns(2)
            
            with col1:
                axis.bar(x.index, x.values, color = 'red')
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)
                
            with col2:
                st.dataframe(new_df)
                
        
        # WordCloud
        st.title("WordCloud")
        df_wc = helper.create_wordcloud(selected_user, df)
        fig, axis = plt.subplots()
        axis.imshow(df_wc)
        st.pyplot(fig)
        
        # Most common words
        
        st.title("Most Common Words")
        most_common_df = helper.most_common_words(selected_user, df)
        
        fig, axis = plt.subplots()
        axis.barh(most_common_df[0], most_common_df[1], color = 'crimson')
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)
        
        
        
        # Emojiy Analysis
        
        emoji_df = helper.emoji_helper(selected_user, df)
        
        st.title("Emoji Analysis")
        
        plt.rcParams['font.family'] = ['Segoe UI Emoji']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.dataframe(emoji_df)
            
        with col2:
            
            # Use only top 10 emojis to avoid clutter
            top_emojis = emoji_df.head(10)
            
            fig, ax = plt.subplots()
            ax.pie(
                top_emojis['Count'],
                labels=top_emojis['Emoji'],
                autopct="%0.2f%%",
                textprops={'fontsize': 14}   
            )
            ax.axis("equal")
            st.pyplot(fig)