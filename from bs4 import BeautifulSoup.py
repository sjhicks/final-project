# import requests
# from bs4 import BeautifulSoup



# url = "https://spotifycharts.com/regional"
# resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# soup = BeautifulSoup(resp.content, 'html.parser')
# #print(soup)
# tup_list = []
# table = soup.find('table', class_ = 'chart-table')
# for artist_data in table.find_all('tr')[1:]:
#     track_name = artist_data.find('td', class_ = 'chart-table-track').contents[0].text
#     artist = artist_data.find('td', class_ = 'chart-table-track').contents[1].text[2:]
#     streams = artist_data.find('td', class_ = 'chart-table-streams').text
#     rank = artist_data.find('td', class_ = 'chart-table-position').text
#     tup_list.append(track_name, artist, streams, rank)
# print(tup_list)
#streams = {}
# for artist in soup.findAll('td', class_ = 'chart-table-track'):
#     for new in artist.findAll('span'):
#         dic[new] = dic.get(new,0) + 1
# sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
# print(sorted_dic)
#var = soup.findAll('td', class_ = 'chart-table-track')
#print(var)
# for artist in soup.findAll('td', class_ = 'chart-table-track'):
#     print(artist)
#     art = artist.find('span')
#     text = art.text.strip()
#     artist_name = text.replace("by ", "")
#     dic[artist_name] = dic.get(artist_name, 0) +1
# sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    
# print(sorted_dic[:10])
#     #for new in artist.findAll('span'):

# num_streams = {}     
# for artist in soup.findAll('td', class_ = 'chart-table-track'):
#     art = artist.find('span')
#     text = art.text.strip()
#     artist_name = text.replace("by ", "")
#     #for streams in soup.findAll('td', class_ = 'chart-table-streams'):
#         #number = streams.text.strip()
#         #num_streams.append(number)
#         #num_streams[artist_name] = dic.get(artist_name, 0) + streams
# #print(num_streams)



# top_ten = sorted_dic[:10]
# #print(top_ten)

import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import sqlite3
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np




url = "https://spotifycharts.com/regional/us/daily/"
resp = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
# page= urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(resp.content, 'html.parser')
# infile=urllib.request.urlopen(page).read()
# data = infile.decode('ISO-8859-1')
#print(soup)
tup_list = []
dic = {}
streams_dic = {}
table = soup.find('table', class_ = 'chart-table')
for artist_data in table.find_all('tr')[1:]:
    track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
    artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
    streams = artist_data.find('td', class_ = 'chart-table-streams').text
    rank = artist_data.find('td', class_ = 'chart-table-position').text
    #tup_list.append((track_name, artist, streams, rank))
    #streams = int(streams)
    dic[artist] = dic.get(artist, 0) +1
    streams_dic[artist] = streams_dic.get(artist, streams) + streams

sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
sorted_streams = sorted(streams_dic.items(), key = lambda x:x[1], reverse = True)

#creating a function to find the artist that appears the most on the charts
def first_artist():
    dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        dic[artist] = dic.get(artist, 0) +1
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    return sorted_dic[0][0]

def second_artist():
    dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        dic[artist] = dic.get(artist, 0) +1
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    return sorted_dic[1][0]
def third_artist():
    dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        dic[artist] = dic.get(artist, 0) +1
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    return sorted_dic[2][0]

def fourth_artist():
    dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        dic[artist] = dic.get(artist, 0) +1
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    return sorted_dic[3][0]

def fifth_artist():
    dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        dic[artist] = dic.get(artist, 0) +1
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    return sorted_dic[4][0]





print(sorted_dic[:10])
#print(sorted_streams)
number_one_artist = sorted_streams[0][0]
number_two_artist = sorted_streams[1][0]
number_three_artist = sorted_streams[2][0]
number_four_artist = sorted_streams[3][0]
number_five_artist = sorted_streams[4][0]
number_six_artist = sorted_streams[5][0]
number_seven_artist = sorted_streams[6][0]
number_eight_artist = sorted_streams[7][0]
number_nine_artist = sorted_streams[8][0]
number_ten_artist = sorted_streams[9][0]

def setUpDatabase(db_name):
     path = os.path.dirname(os.path.abspath(__file__))
     conn = sqlite3.connect(path+'/'+db_name)
     cur = conn.cursor()
     return cur, conn

def setUpSongTable(first, second, third, fourth, fifth, cur,conn):
    cur.execute('DROP TABLE IF EXISTS streams')
    cur.execute('CREATE TABLE IF NOT EXISTS streams("Artist TEXT" TEXT Primary Key, "Streams" TEXT)')
    
if __name__ == "__main__":
    first  = first_artist()
    second = second_artist()
    third = third_artist()
    fourth = fourth_artist()
    fifth = fifth_artist()
    #print(first, second, third, fourth, fifth)
    
    conn = sqlite3.connect('steams.sqlite')
    cur = conn.cursor()
    setUpSongTable(first, second, third, fourth, fifth, cur, conn)