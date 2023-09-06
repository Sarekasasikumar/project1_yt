#!/usr/bin/env python
# coding: utf-8

# In[4]:


import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector as sql
import pymongo

# Function to execute SQL queries
def execute_sql_query(query):
    try:
        connection = sql.connect(
            host="localhost",
            user="root",
            password="sarika_600",
            database="youtube_new1"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("YouTube Data Harvesting")

# Sidebar for user input
st.sidebar.header("SQL Query")

# Define a text input for SQL queries
query_input = st.sidebar.text_area("Enter your SQL query:", "")

# Define a button to execute the query
if st.sidebar.button("Execute Query"):
    # Check if a query is entered
    if not query_input:
        st.warning("Please enter an SQL query.")
    else:
        # Execute the query and display results
        query_results = execute_sql_query(query_input)
        if isinstance(query_results, str):
            st.error(f"Query Execution Error: {query_results}")
        else:
            result_df = pd.DataFrame(query_results)
            st.dataframe(result_df)

# Create a MongoDB connection
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['Youtube_new']
collection = db['col_youtube_new']

# Display channel and video data
st.header("Channel Data")

# Loop through channel data and display for multiple channels
channel_ids = [
    'UCW5YeuERMmlnqo4oq8vwUpg',  # the net ninja
    'UC29ju8bIPH5as8OGnQzwJyA',  # traversy media
    'UC5CMtpogD_P3mOoeiDHD5eQ',  # codecademy
    'UCCezIgC97PvUuR4_gbFUs5g',  # corey schafer
    'UCvjgXvBlbQiydffZU7m1_aw',  # the coding train
    # Add more channel IDs here
]

for channel_id in channel_ids:
    channel_data = collection.find_one({'channel_id': channel_id})
    if channel_data:
        st.write(f"Channel Name ({channel_id}): {channel_data['channel_name']}")
        st.write(f"Subscribers: {channel_data['subscribers']}")
        st.write(f"Total Videos: {channel_data['total_videos']}")

st.header("Video Data")

# Loop through video data for multiple channels
for channel_id in channel_ids:
    st.subheader(f"Videos for Channel {channel_id}")
    video_data = collection.find({'channel_id': channel_id})
    for video in video_data:
        if 'title' in video:
            st.write("Video Title:", video['title'])
        else:
            st.write("Video Title: N/A")
        if 'description' in video:
            st.write("Description:", video['description'])
        else:
            st.write("Description: N/A")
        st.write("---")

# Example SQL query
st.sidebar.markdown("## Example Queries")
example_queries = [
    "SELECT * FROM channels0;",
    "SELECT channel_name, subscribers FROM channels0 WHERE subscribers > 1000000;",
    "SELECT video_id, title FROM videos0 WHERE video_id = '12345';"
]

selected_example = st.sidebar.selectbox("Choose an example query:", example_queries)
if st.sidebar.button("Execute Example"):
    query_input = selected_example
    query_results = execute_sql_query(query_input)
    if isinstance(query_results, str):
        st.error(f"Query Execution Error: {query_results}")
    else:
        result_df = pd.DataFrame(query_results)
        st.dataframe(result_df)

# Add sections for your specific queries
st.sidebar.header("Specific Queries")

# Query 1: What are the names of all the videos and their corresponding channels?
if st.sidebar.button("Query 1: Names of all videos and their corresponding channels"):
    query_results = execute_sql_query("SELECT channel_name, title FROM videos0;")
    if isinstance(query_results, str):
        st.error(f"Query Execution Error: {query_results}")
    else:
        result_df = pd.DataFrame(query_results)
        st.header("Query 1 Results: Names of all videos and their corresponding channels")
        st.dataframe(result_df)

# Query 2: Which channels have the most number of videos, and how many videos do they have?
if st.sidebar.button("Query 2: Channels with most videos"):
    query_results = execute_sql_query("SELECT channel_name, MAX(total_videos) AS max_videos FROM channels0;")
    if isinstance(query_results, str):
        st.error(f"Query Execution Error: {query_results}")
    else:
        result_df = pd.DataFrame(query_results)
        st.header("Query 2 Results: Channels with the most videos")
        st.dataframe(result_df)

# Add more sections for other specific queries (3 to 10)

# Close MongoDB connection
client.close()


# In[5]:


import streamlit as st
import pandas as pd
from googleapiclient.discovery import build

# Initialize the YouTube Data API client with your API key
api_key = "AIzaSyBLoyVMDML5ueT9pqqTi-7Krjk2g7RcNFk"  # Replace with your actual API key
youtube = build("youtube", "v3", developerKey=api_key)

# Function to retrieve channel data using the API
def get_channel_data(channel_id):
    try:
        response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        ).execute()

        if 'items' in response:
            channel = response['items'][0]
            return channel
        else:
            return None
    except Exception as e:
        return str(e)

# Function to retrieve video data using the API
def get_video_data(video_id):
    try:
        response = youtube.videos().list(
            part="snippet",
            id=video_id
        ).execute()

        if 'items' in response:
            video = response['items'][0]
            return video
        else:
            return None
    except Exception as e:
        return str(e)
# Function to execute SQL queries
def execute_sql_query(query):
    try:
        connection = sql.connect(
            host="localhost",
            user="root",
            password="sarika_600",
            database="youtube_new1"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        connection.close()
        return results
    except Exception as e:
        return str(e)

# Function to retrieve data from MongoDB
def get_mongodb_data(collection_name, filter_query={}):
    try:
        client = pymongo.MongoClient('mongodb://localhost:27017/')
        db = client['Youtube_new']  # Replace with your actual MongoDB database name
        collection = db['col_youtube_new']
        data = collection.find(filter_query)
        return data
    except Exception as e:
        return str(e)

# Streamlit UI
st.title("YouTube Data Harvesting")

# Sidebar for user input
st.sidebar.header("Channel and Video IDs")

# Define text inputs for channel and video IDs
channel_id_input = st.sidebar.text_input("Enter Channel ID:", "")
video_id_input = st.sidebar.text_input("Enter Video ID:", "")

# Define buttons to retrieve data
if st.sidebar.button("Get Channel Data"):
    if not channel_id_input:
        st.warning("Please enter a Channel ID.")
    else:
        channel_data = get_channel_data(channel_id_input)
        if channel_data:
            st.header("Channel Data")
            st.write(f"Channel Name: {channel_data['snippet']['title']}")
            st.write(f"Subscribers: {channel_data['statistics']['subscriberCount']}")
            st.write(f"Total Videos: {channel_data['statistics']['videoCount']}")
        else:
            st.warning("No channel data found.")

if st.sidebar.button("Get Video Data"):
    if not video_id_input:
        st.warning("Please enter a Video ID.")
    else:
        video_data = get_video_data(video_id_input)
        if video_data:
            st.header("Video Data")
            st.write(f"Video Title: {video_data['snippet']['title']}")
            st.write(f"Description: {video_data['snippet']['description']}")
        else:
            st.warning("No video data found.")

# Add a section to query your MongoDB and display results
st.sidebar.header("MongoDB Query")

# Define a text input for MongoDB queries
mongodb_query_input = st.sidebar.text_area("Enter your MongoDB query:", "")

# Define a button to execute the MongoDB query
if st.sidebar.button("Execute MongoDB Query"):
    if not mongodb_query_input:
        st.warning("Please enter a MongoDB query.")
    else:
        # Parse and execute the MongoDB query
        try:
            collection_name = "YourMongoDBCollection"  # Replace with your actual MongoDB collection name
            filter_query = eval(mongodb_query_input)  # Assuming filter_query is a dictionary
            mongodb_data = get_mongodb_data(collection_name, filter_query)
            if mongodb_data:
                st.header("MongoDB Query Results")
                for item in mongodb_data:
                    st.write(item)
            else:
                st.warning("No MongoDB data found.")
        except Exception as e:
            st.error(f"MongoDB Query Error: {str(e)}")

# Add a section to execute SQL queries and display results
st.sidebar.header("SQL Query")

# Define a text input for SQL queries
sql_query_input = st.sidebar.text_area("Enter your SQL query:", "")

# Define a button to execute the SQL query
if st.sidebar.button("Execute SQL Query"):
    if not sql_query_input:
        st.warning("Please enter an SQL query.")
    else:
        # Execute the SQL query and display results
        query_results = execute_sql_query(sql_query_input)
        if isinstance(query_results, str):
            st.error(f"SQL Query Execution Error: {query_results}")
        else:
            result_df = pd.DataFrame(query_results)
            st.header("SQL Query Results")
            st.dataframe(result_df)


# In[ ]:




