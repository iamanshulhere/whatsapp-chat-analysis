import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt

st.sidebar.title("What'sapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    
    data = bytes_data.decode("utf-8")
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
                
            