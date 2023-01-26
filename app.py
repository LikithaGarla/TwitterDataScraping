import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import snscrape.modules.twitter as sntwitter
import itertools
import pymongo
from pymongo import MongoClient
import datetime
import pyautogui

global collection
data = pd.DataFrame()

def InitializeConnection():
  global collection
  uri = 'mongodb://MongoDb:<password>@ac-jdflryq-shard-00-00.ciatbst.mongodb.net:27017,ac-jdflryq-shard-00-01.ciatbst.mongodb.net:27017,ac-jdflryq-shard-00-02.ciatbst.mongodb.net:27017/?ssl=true&replicaSet=atlas-kn8q2t-shard-0&authSource=admin&retryWrites=true&w=majority'
  conn = MongoClient( uri )
  db = conn.likitha
  collection = db.ScrapeData

def Upload_to_Database():
  data_list = data.values.tolist()
  collection.insert_one({word : data_list})

def Twitter_Scrap(search_text,from_date,to_date,count):
  global data
  since = from_date.strftime("%Y-%m-%d")
  until=to_date.strftime("%Y-%m-%d")
  s  = search_text +' '+'since:'+since+' '+'until:'+until
  data = pd.DataFrame(itertools.islice(sntwitter.TwitterSearchScraper(
    s).get_items(), count))
  
def Search_Button_Clicked():
  data =  Twitter_Scrap(word,from_date,to_date,limit_number)
  pyautogui.hotkey("ctrl","F5")

def Click():
  st.write('Button is Clicked')

def Display_Data():
  st.write(data.values)
  if st.button("Upload to Database"):
    Upload_to_Database()
  if st.button("Download as CSV"):
    data.to_csv('SampleFile.csv')
  if st.button("Download as Json"):
    data.to_json('SampleFile1.json')
    

InitializeConnection()
st.title('Twitter Data Scrapping')
word = st.text_input('Enter Keyword or Hashtag to search')
from_date = st.date_input('Enter the starting date range')
to_date = st.date_input('Enter the ending date')
limit_number = st.number_input('Enter no. of records to search', 0, 5000)
if st.button("Search Data"):
  Search_Button_Clicked()
  Display_Data()
