import matplotlib.pyplot as plt
from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji

extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch total number of words
    words = []
    for m in df['message']:
        words.extend(m.split())
    
    # fetch umber of media messages
    num_media_message = df[df['message'] == "<Media omitted>\n"].shape[0]

    # fetch number of links shared
    links = []
    for m in df['message']:
        links.extend(extract.find_urls(m))

        
    return num_messages,words,num_media_message,len(links)



def Most_busy_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts()/ df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    return x,df



def create_wordcloud(selected_user,df):

    f = open('stopwords.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # this will include stop words but t hey are of no use then need to perform few steps
    # remove group messages/notification
    temp = df[df['user'] !='group_notification']
    # remove media omitted message
    temp = temp[temp['message'] != '<Media omitted>\n']

    def remove_stop_words(message):
        y = []
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message'] = temp['message'].apply(remove_stop_words)
    df_wc = wc.generate(temp['message'].str.cat(sep=" ")) #df-> temp
    return df_wc

def most_common_words(selected_user,df):

    f = open('stopwords.txt','r')
    stop_words = f.read()

    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    # this will include stop words but t hey are of no use then need to perform few steps
    # remove group messages/notification
    temp = df[df['user'] !='group_notification']
    # remove media omitted message
    temp = temp[temp['message'] != '<Media omitted>\n']
    # remove stop word
    # some words are in hindi and other language  
    words = []
    for m in temp['message']:
        for word in m.lower().split():
            if word not in stop_words:
                words.append(word)
    
    
    clean_df = pd.DataFrame(Counter(words).most_common(20))
    return clean_df

#emoji analysis
# def emojiTimeline(selected_user,df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []
#     for m in df['message']:
#         emojis.extend([c for c in m if c in emoji.UNICODE_EMOJI['en']])
    
#     emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

#     return emoji_df

# def is_emoji(char):
#     return char in emoji.UNICODE_EMOJI_ENGLISH

# def emojiTimeline(selected_user, df):
#     if selected_user != 'Overall':
#         df = df[df['user'] == selected_user]

#     emojis = []
#     for message in df['message']:
#         for char in message:
#             if is_emoji(char):
#                 emojis.append(char)

#     emoji_counts = Counter(emojis)
#     emoji_df = pd.DataFrame(list(emoji_counts.items()), columns=['Emoji', 'Count'])
#     emoji_df = emoji_df.sort_values(by='Count', ascending=False)

#     return emoji_df



# def montly timeline

def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()

    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+ str(timeline['year'][i]))
                    
    timeline['time']=time

    return timeline


def daily_Timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    dailychat = df.groupby('onlyDate').count()['message'].reset_index()
    
    return dailychat


def week_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()


def Month_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    return df['month'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    
    user_heatmap = df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    
    return user_heatmap
