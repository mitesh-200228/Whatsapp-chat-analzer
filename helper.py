import streamlit
from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
from wordcloud import WordCloud
extract = URLExtract()

def fetchData(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    num_message = df.shape[0]
    words = []
    for message in df['message']:
        words.extend(message.split())

    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    if selected_users == 'Overall':
        top5 = df['user'].count()

    return num_message,len(words),num_media_messages,len(links)

def most_busy(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'index': 'name', 'user': 'percent'})
    return x,df

def create_wordcloud(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    wc = WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    df_wc = wc.generate((df['message'].str.cat(sep=" ")))
    return df_wc

def most_common_word(selected_users,df):

    f = open("stop_hinglish.txt",'r')
    stop_words = f.read()

    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    return_df = pd.DataFrame(Counter(words).most_common(20))
    return_df[0] = return_df[0].str.replace('\d+',' ')
    return_df.rename(columns={'0':'Words','1':'Counts'})
    return return_df

def emoji_helper(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df

def monthly_timline(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    timeline = df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))

    timeline['time'] = time

    return timeline

def daily_timeline(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    daily_timelines = df.groupby('only_date').count()['message'].reset_index()
    return daily_timelines

def week_activity_map(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    return df['name_of_day'].value_counts()

def month_map(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    return df['month_map'].value_counts()

def heatmap(selected_users,df):
    if selected_users != 'Overall':
        df = df[df['user'] == selected_users]

    heatm = df.pivot_table(index='name_of_day',columns='period',values='message',aggfunc='count').fillna(0)
    return heatm