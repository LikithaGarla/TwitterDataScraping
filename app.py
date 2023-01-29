%%writefile app.py
import streamlit as st
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import pymongo
from pymongo import MongoClient
import datetime
from google.colab import files
from time import sleep

data = pd.DataFrame()

def InitializeConnection():
  global collection
  uri = 'mongodb://MongoDb:MongoDbGUVI@ac-jdflryq-shard-00-00.ciatbst.mongodb.net:27017,ac-jdflryq-shard-00-01.ciatbst.mongodb.net:27017,ac-jdflryq-shard-00-02.ciatbst.mongodb.net:27017/?ssl=true&replicaSet=atlas-kn8q2t-shard-0&authSource=admin&retryWrites=true&w=majority'
  conn = MongoClient( uri )
  db = conn.likitha
  collection = db.ScrapeData

def Upload_to_Database():
  placeholder.empty()
  data_list = data.values.tolist()
  recordKey = word+'_'+str(datetime.datetime.now().timestamp())
  collection.insert_one({word : data_list})
  placeholder.write("Successfully Uploaded to Database")

def Twitter_Scrap(search_text,from_date,to_date,count):
  global data
  since = from_date.strftime("%Y-%m-%d")
  until=to_date.strftime("%Y-%m-%d")
  s  = search_text +' '+'since:'+since+' '+'until:'+until
  data = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
    s).get_items(), count))
  
def Search_Button_Clicked():
  data =  Twitter_Scrap(word,from_date,to_date,limit_number)

InitializeConnection()
st.title('Twitter Data Scrapping')
placeholder = st.empty()
flag=0
with placeholder.container():
  word = st.text_input('Enter Keyword or Hashtag to search')
  from_date = st.date_input('Enter the starting date range')
  to_date = st.date_input('Enter the ending date')
  limit_number = st.number_input('Enter no. of records to search', 0, 5000)
  if st.button("Search Data"):
    placeholder.empty()
    Search_Button_Clicked()
    flag=1
if flag==1:
  placeholder.empty()
  sleep(0.01)
  with placeholder.container():
    col1, col2, col3 = st.columns([1,1,1])
    with col1:
      st.button("Upload to Database",key=None,on_click=Upload_to_Database)
    with col2:
      st.download_button(
        label="Download as CSV",
        data=data.to_csv().encode('utf-8'),
        file_name=word+'.csv',
        mime='text/csv')
    with col3:
      st.download_button(
        label="Download as Json",
        data=data.to_json().encode('utf-8'),
        file_name=word+'.json',
        mime='application/json')
    st.table(data)

