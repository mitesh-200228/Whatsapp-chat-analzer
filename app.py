import streamlit as st
import preprocessor,helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analizer")

uploaded_file = st.sidebar.file_uploader("Choose a file")

if uploaded_file is not None:
     bytes_data = uploaded_file.getvalue()
     data = bytes_data.decode('utf-8')
     df = preprocessor.func(data)

     userlist = df['user'].unique().tolist()
     userlist.remove('group_notification')
     userlist.sort()
     userlist.insert(0,"Overall")

     selected_users = st.sidebar.selectbox("Show analysis with respect to",userlist)

     if st.sidebar.button("Show Analysis"):

          num_messages,words,num_media_messages,links = helper.fetchData(selected_users,df)
          st.title("Top Statistics")
          col1,col2,col3,col4 = st.columns(4)
          with col1:
               st.header("Total Messages")
               st.title(num_messages)
          with col2:
               st.header("Total Words")
               st.title(words)
          with col3:
               st.header("Media Uploaded")
               st.title(num_media_messages)
          with col4:
               st.header("Total Links Uploaded")
               st.title(links)

          #timeline
          st.title("Monthly Timeline")
          timeline = helper.monthly_timline(selected_users,df)
          fig,ax = plt.subplots()
          ax.plot(timeline['time'],timeline['message'],color='blue')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          #its daily timeline broo
          st.title("Per Day Timeline")
          daily_timeline = helper.daily_timeline(selected_users,df)
          fig,ax = plt.subplots()
          ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='green')
          plt.xticks(rotation='vertical')
          st.pyplot(fig)

          ####
          st.title('Map')
          col1,col2 = st.columns(2)
          with col1:
               st.header('Most Busy Day List')
               busy_day = helper.week_activity_map(selected_users, df)
               fig,ax = plt.subplots()
               ax.bar(busy_day.index,busy_day.values)
               plt.xticks(rotation='vertical')
               st.pyplot(fig)
          with col2:
               st.header('Most Busy Month List')
               months = helper.month_map(selected_users, df)
               fig,ax = plt.subplots()
               ax.bar(months.index,months.values,color='purple')
               plt.xticks(rotation='vertical')
               st.pyplot(fig)

          st.title("Heat Map of weekly activation of users")
          heatm = helper.heatmap(selected_users,df)
          fig,ax = plt.subplots()
          ax = sns.heatmap(heatm)
          st.pyplot(fig)
          # st.pyplot(sns.heatmap(heatm))

          if selected_users == 'Overall':
               st.title("Most busy Users")
               top5,new_df = helper.most_busy(df)
               fig,ax = plt.subplots()
               col1,col2 = st.columns(2)

               with col1:
                    ax.bar(top5.index, top5.values,color="red")
                    plt.xticks(rotation='vertical')
                    st.pyplot(fig)
               with col2:
                    st.dataframe(new_df)
          #WordCloud
          st.title("WordClouds")
          df_wc = helper.create_wordcloud(selected_users,df)
          fig,ax = plt.subplots()
          plt.imshow(df_wc)
          st.pyplot(fig)

          #Most Common Word
          most_common_df = helper.most_common_word(selected_users,df)
          fig,ax = plt.subplots()
          ax.barh(most_common_df[0],most_common_df[1])
          st.title('Most Common Words')
          st.pyplot(fig)

          #Emoji Counter
          emoji_df = helper.emoji_helper(selected_users,df)
          st.title("Emojis Analysis")

          col1,col2 = st.columns(2)

          with col1:
               st.dataframe(emoji_df)
          with col2:
               fig,ax = plt.subplots()
               ax.pie(emoji_df[1].head(),labels=emoji_df[0].head(),autopct="%0.2f")
               st.pyplot(fig)