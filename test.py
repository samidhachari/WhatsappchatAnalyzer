import streamlit as st
import preprocessor
import matplotlib.pyplot as plt
import seaborn as sns



st.sidebar.title("Whatsapp Chat Analyzer")
uploadedFile = st.sidebar.file_uploader("Upload your file")
if uploadedFile is not None:
    # to read files as byte
    bytes_data = uploadedFile.getvalue()
    data = bytes_data.decode("utf-8")
    # st.text(data)
    df = preprocessor.preprocessing_data(data)

    from stats import fetch_stats,Most_busy_users,most_common_words,create_wordcloud,monthly_timeline,daily_Timeline,week_activity_map,Month_activity_map,activity_heatmap


    st.dataframe(df)
    # fetch unique user
    user_list = df['user'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt ",user_list)

    if st.sidebar.button("Show Analysis"):
        num_messages, words, num_media_messages , num_links  = fetch_stats(selected_user,df)
        st.title('Top Statistics')
        cols = st.columns(4)  # Create 4 columns

        
        with cols[0]:
            st.header("Total Messages")
            st.title(num_messages)
        with cols[1]:
            st.header("Total Words")
            st.title(len(words))
        with cols[2]:
            st.header("Media Shared")
            st.title(num_media_messages)
        with cols[3]:
            st.header("Links Shared")
            st.title(num_links)


    #timeline
    st.title("Monthly Timeline")
    timeline = monthly_timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(timeline['time'],timeline['message'],color='green')
    plt.xticks(rotation ='vertical')
    st.pyplot(fig)

    # daily timeline
    st.title("Daily Timeline")
    dailyTimeline = daily_Timeline(selected_user,df)
    fig,ax = plt.subplots()
    ax.plot(dailyTimeline['onlyDate'],dailyTimeline['message'],color='black')
    plt.xticks(rotation ='vertical')
    st.pyplot(fig)

    # activity map day 
    st.title("Activity Map ")
    cols = st.columns(2)
    with cols[0]:
        st.header("Most Busy Day")
        busy_day = week_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_day.index,busy_day.values)
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)

    with cols[1]:
        st.header("Most Busy Month")
        busy_Month = Month_activity_map(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(busy_Month.index,busy_Month.values)
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)
    

    st.title("User Weekly Activity HeatMap")
    user_heatmap = activity_heatmap(selected_user,df)
    fig,ax = plt.subplots()
    ax = sns.heatmap(user_heatmap)
    plt.xticks(rotation ='vertical')
    st.pyplot(fig)
    



    # find busiest users in group not user level
    if selected_user == 'Overall':
        st.title('Most Busy Users')
        x , new_df= Most_busy_users(df)
        fig, ax = plt.subplots() 
        cols = st.columns(2)


# bar cart and dataframe in percent form user chat
        with cols[0]:
            ax.bar(x.index,x.values,color='red')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with cols[1]:
            st.dataframe(new_df)
            
        #wordcloud
    st.title('Word Cloud')
    df_wc = create_wordcloud(selected_user,df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)
    # most common words
    st.title('Most Common Words')
    mcw_df = most_common_words(selected_user,df)

    fig,ax = plt.subplots()
    ax.barh(mcw_df[0],mcw_df[1])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)
    # st.dataframe(mcw_df)

    #emoji analysis
    # st.title("Most Common Emoji")
    # emoji_df = emojiTimeline(selected_user,df)
    # st.dataframe(emoji_df)

    # which member is most active on which day of week and month in chat 
        
# know heatmap on which time the user are active on week
    