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
import matplotlib
import matplotlib.pyplot as plt



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
    
    return final_result

def get_averages(lst):
    average_streams = []
    for artist in lst:
        average = artist[1]/ artist[2]
        average_streams.append((artist[0],artist[1],artist[2],average))
    sorted_average = sorted(average_streams, key = lambda x:x[3], reverse = True)
    return(sorted_average)
    

def setUpDatabase(db_name):
     path = os.path.dirname(os.path.abspath(__file__))
     conn = sqlite3.connect(path+'/'+db_name)
     cur = conn.cursor()
     return cur, conn

def setUpSongTable(first, average, cur,conn):
    cur.execute('DROP TABLE IF EXISTS streams')
    cur.execute('CREATE TABLE IF NOT EXISTS streams(Artist TEXT PRIMARY KEY, Streams INTEGER, Occurance INTEGER, Average REAL)')
    for artist in average:
        cur.execute("INSERT INTO streams (Artist, Streams, Occurance, Average) VALUES (?,?,?,?)", (artist[0], artist[1],artist[2],artist[3]))
    conn.commit()
    # for i in average:
    #     cur.execute("INSERT INTO streams (Occurance, Average) VALUE (?)", (i[1]))
    # conn.commit()

    # for i in range(len(sorted_streams)):
    #     cur.execute("INSERT INTO Categories (artist),streams) VALUES (?,?)",(sorted_streams[i][0],sorted_streams[i][1]))
    # conn.commit()

def barchart_averages():
    cur.execute("SELECT * FROM streams")
    label_name = []
    average_streams = []
    for row in average:
        label_name.append(row[0])
    for row2 in average:
        average_streams.append(row2[3])
        
    #print("LABEL NAMEMEMMEMEMEMMEMEE")
    #print(label_name)


    labels = [label_name[0], label_name[1],label_name[2],label_name[3], label_name[4],label_name[5], label_name[6],label_name[7],label_name[8], label_name[9]]
    avg_streams = [average_streams[0],average_streams[1], average_streams[2],average_streams[3],average_streams[4], average_streams[5], average_streams[6],average_streams[7],average_streams[8], average_streams[9]]
    plt.bar(labels, avg_streams, align = "center", color = ["red", "pink", "lightpink", "green", "deeppink", "navy", "lightblue", "lightgreen","purple","pink"])
    plt.title("Comparison of Average Streams for Artists on the Top 200 Charts")
    plt.ylabel("Average Song Streams (by the millions)")
    plt.xlabel("Artist Name")
    plt.savefig("artist_streams.png")
    plt.show()
    
    return ((label_name[0], average_streams[0]),(label_name[1], average_streams[1]), (label_name[2], average_streams[2]), (label_name[3], average_streams[3]), (label_name[4], average_streams[4]), (label_name[5], average_streams[5]), (label_name[6], average_streams[6]),(label_name[7], average_streams[7]), (label_name[8], average_streams[8]), (label_name[9], average_streams[9]))


if __name__ == "__main__":
    first  = first_artist()
    average = get_averages(first)
    cur, conn = setUpDatabase('streams.db')
    setUpSongTable(first, average,cur,conn)
    barchart_averages()
    