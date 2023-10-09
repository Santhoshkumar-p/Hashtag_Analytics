import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
#st.title("Hashtag Analytics")

# Add a selectbox to the sidebar:
#add_selectbox = st.sidebar.selectbox(
#    'How would you like to be contacted?',
#    ('Email', 'Home phone', 'Mobile phone')
#)

# Add a slider to the sidebar:
#add_slider = st.sidebar.slider(
#    'Select a range of values',
#    0.0, 100.0, (25.0, 75.0)
#)


#Header
h1,h2,h3,h4 = st.columns([0.25,0.25,0.25,0.25])
h1.text('Hashtag Analytics')
h2.text_input(label="", label_visibility="collapsed", placeholder="Enter a hashtag", value="")
#center_column.button("Search")
h4.download_button("Get Full Report","")

#Metrics Bar
m1,m2,m3,m4,m5,m6,m7 = st.columns([0.05,0.18,0.18,0.18,0.18,0.18,0.05],gap='small')
m1.write("")
m2.metric("Mentions", value="300K", delta="1.5k")
m3.metric("Interactions", value="24K", delta="-345")
m4.metric("Reach", value="1M", delta="768")
m5.metric("Shares", value="67K", delta="98")
m6.metric("Likes", value="100.4K", delta="-15k")
m7.write("")

#Latest Mentions
l1, l2 = st.columns([0.65, 0.35])
with l1.container():
    st.write('Latest Mentions')
    mentions_df = pd.DataFrame([
        {"Post": "🍁 Fall in Love with Savings 🛍️...","site":"youtube", "date": 4, "mood": True},
       {"Post": "🍁 Fall in Love with Savings 🛍️...", "site":"instagram","date": 5, "mood": False},
       {"Post": "🍁 Fall in Love with Savings 🛍️...", "date": 3, "mood": True},
       
    ])
    st.data_editor(mentions_df, num_rows="dynamic")
with l2.container():
    st.write('Top Influencers')
    influencers_df = pd.DataFrame([
        {"dp": "🛍️","Id":"@tom", "# of follower": "400k"},
       {"dp": "🛍️","Id":"@tom", "# of follower": "400k"},
       {"dp": "🛍️","Id":"@tom", "# of follower": "400k"}
    ])
    related_hashtags_df = pd.DataFrame([
        {"Hashtag": "trend","No. of uses":234},
       {"Hashtag": "fashion","No. of uses":234},
       {"Hashtag": "lifestyle","No. of uses":234},
    ])
    st.data_editor(influencers_df, num_rows="dynamic",key="influencer")
    st.write('Related hashtags')
    st.data_editor(related_hashtags_df, num_rows="dynamic",key='influencers')

#Analytics
a1, a2, a3 = st.columns(3)
with a1.container():
    st.write('Reach')
    st.write('No of views per day')
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
with a2.container():
    st.write('Interactions')
    st.write('No of engagements per day')
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.bar_chart(chart_data)
with a3.container():
    st.write('Google Search Trends')
    st.write('Searches/Month')
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)

#WorldMap
heatmap = st.container()
heatmap.write('Trending all over the world')
heatmap_df = pd.DataFrame(
np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
columns=['lat', 'lon'])
heatmap.map(heatmap_df)

#Analytics 2
a1, a2, a3 = st.columns(3)
with a1.container():
    st.write('Sources')
    
    sources = st.selectbox('Source', ['instagram', 'Youtube', 'Tiktok'])
    platform_data = {
    'Platforms': ['Instagram', 'Youtube', 'Tiktok'],
    'instagram': [12, 1, 20,],
    'youtube': [4,4, 12],
    'tiktok': [24, 7, 62]}
    fig = px.pie(platform_data, values=sources, names='Platforms',
                 title=f'number of {sources} mentions',
                 height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)

with a2.container():
    st.write('Languages')
    
    sources = st.selectbox('Language', ['english', 'spanish', 'french'])
    platform_data = {
    'languages': ['english', 'spanish', 'french'],
    'english': [12, 1, 20,],
    'spanish': [4,4, 12],
    'french': [24, 7, 62]}
    fig = px.pie(platform_data, values=sources, names='languages',
                 title=f'number of {sources} mentions',
                 height=300, width=200)
    fig.update_layout(margin=dict(l=20, r=20, t=30, b=0),)
    st.plotly_chart(fig, use_container_width=True)
with a3.container():
    st.write('Mentions by Weekday')
    chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])
    st.line_chart(chart_data)

