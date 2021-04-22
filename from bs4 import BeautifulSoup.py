import requests
from bs4 import BeautifulSoup
import urllib.request
import json
import sqlite3
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import os



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
    streams = streams.replace(",", "")
    rank = artist_data.find('td', class_ = 'chart-table-position').text
    tup_list.append((track_name,artist,streams,rank))
    #streams = int(streams)
    dic[artist] = dic.get(artist, 0) +1
    streams_dic[artist] = streams_dic.get(artist, int(streams)) + int(streams)

sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
sorted_streams = sorted(streams_dic.items(), key = lambda x:x[1], reverse = True)
#for i in range(len(sorted_streams)):
    #print(sorted_streams[i][0],sorted_streams[i][1])
    
#print(sorted_streams[:10])
#print(sorted_dic[:10])
#creating a function to find the artist that appears the most on the charts
def first_artist():
    dic = {}
    lst = []
    streams_dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        streams = streams.replace(",", "")
        dic[artist] = dic.get(artist, 0) +1
        streams_dic[artist] = streams_dic.get(artist, int(streams)) + int(streams)
        #lst.append((track_name, streams))
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    number_one = sorted_dic[0][0]
    #print(sorted_dic)
    sorted_streams = sorted(streams_dic.items(), key = lambda x:x[1], reverse = True)
    #print(sorted_streams)
    #print (sorted_streams[0])
    #final_tup_list = []
    result = {}
    for i in sorted_streams:
        result[i[0]] = list(i[:])
    for i in sorted_dic:
        if i[0] in result:
            result[i[0]].extend(list(i[1:]))
    final_result = []
    for i,j in result.items():
        final_result.append(tuple(j))
    print(final_result)
    total_streams = 0
    for item in sorted_streams: 
        if item[0]== number_one:
            total_streams += item[1]
        #final_tup_list.append(item, total_streams)
    
    #final_tup_list = [(number_one, total_streams)]
    #print(final_tup_list)
    
    return final_result

def second_artist():
    dic = {}
    lst = []
    streams_dic = {}
    table = soup.find('table', class_ = 'chart-table')
    for artist_data in table.find_all('tr')[1:]:
        track_name = artist_data.find('td', class_ = 'chart-table-track').contents[1].contents[0]
        artist = artist_data.find('td', class_ = 'chart-table-track').contents[3].text[3:]
        streams = artist_data.find('td', class_ = 'chart-table-streams').text
        streams = streams.replace(",", "")
        dic[artist] = dic.get(artist, 0) +1
        streams_dic[artist] = streams_dic.get(artist, int(streams)) + int(streams)
            #lst.append((track_name, streams))
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    number_one = sorted_dic[0][0]
        #print(sorted_dic)
    sorted_streams = sorted(streams_dic.items(), key = lambda x:x[1], reverse = True)
        #print(sorted_streams)
        #print (sorted_streams[0])
        #final_tup_list = []
    total_streams = 0
    for item in sorted_streams: 
        if item[0]== number_one:
            total_streams += item[1]
        #final_tup_list.append(item, total_streams)
    
    #final_tup_list = [(number_one, total_streams)]
    #print(final_tup_list)
    
    return sorted_dic
    #print(lstt)
    #return final_tup_list

    #for artist in final_tup_list:
        #print(artist[0][0])
   # print(streams_dic)
   # print(number_one)
    #return (total_streams)


    #return sorted_dic[0][0]


#print(sorted_dic[:10])
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

def setUpSongTable(first, cur,conn):
    cur.execute('DROP TABLE IF EXISTS streams')
    cur.execute('CREATE TABLE IF NOT EXISTS streams(Artist TEXT PRIMARY KEY, Streams INTEGER, Occurance INTEGER)')
    for artist in first:
        cur.execute("INSERT INTO streams (Artist, Streams, Occurance) VALUES (?,?,?)", (artist[0], artist[1],artist[2]))
    conn.commit()

    # for i in range(len(sorted_streams)):
    #     cur.execute("INSERT INTO Categories (artist),streams) VALUES (?,?)",(sorted_streams[i][0],sorted_streams[i][1]))
    # conn.commit()
    
if __name__ == "__main__":
    first  = first_artist()
    #second = second_artist()
    # third = third_artist()
    # fourth = fourth_artist()
    # fifth = fifth_artist()
    #print(first, second, third, fourth, fifth)
    cur, conn = setUpDatabase('streams.db')
    setUpSongTable(first, cur,conn)
    #conn = sqlite3.connect('streams.db')
    #cur = conn.cursor()
    #setUpSongTable(cur,conn)