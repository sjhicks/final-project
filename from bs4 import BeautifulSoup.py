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

soup = BeautifulSoup(resp.content, 'html.parser')

#creating a function to find information on artists that are on Spotify's top 200 charts
#the info includes the artist's name, total amount of streams, and how often they are on the charts
def find_artist_info():
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
    sorted_dic = sorted(dic.items(), key = lambda x:x[1], reverse = True)
    number_one = sorted_dic[0][0] 
    sorted_streams = sorted(streams_dic.items(), key = lambda x:x[1], reverse = True)

    #combining the two dictionaries into a tuble list
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

#this function finds the average amount of streams an artist gets on the charts 

# def get_averages(lst):
#     average_streams = []
#     for artist in lst:
#         average = artist[1]/ artist[2]
#         average_streams.append((artist[0],artist[1],artist[2],average))
#     sorted_average = sorted(average_streams, key = lambda x:x[3], reverse = True)
#     return(sorted_average)
    

def setUpDatabase(db_name):
     path = os.path.dirname(os.path.abspath(__file__))
     conn = sqlite3.connect(path+'/'+db_name)
     cur = conn.cursor()
     return cur, conn

def setUpSongTable(info, cur,conn):
    cur.execute('DROP TABLE IF EXISTS streams')
    cur.execute('CREATE TABLE IF NOT EXISTS streams(Artist TEXT PRIMARY KEY, Streams INTEGER, Occurance INTEGER)')
    for artist in info:
        cur.execute("INSERT INTO streams (Artist, Streams, Occurance) VALUES (?,?,?)", (artist[0], artist[1],artist[2]))
    conn.commit()

def get_averages(cur,conn):
    cur.execute("SELECT Artist, Streams, Occurance FROM streams")
    info= cur.fetchall()
    print("HIIIII") 
    average_lst = []
    for artist in info:
        average = artist[1] / artist[2]
        average_lst.append((artist[0],average))
    sorted_average = sorted(average_lst, key = lambda x:x[1], reverse = True)
    return(sorted_average)

def setUpAverageTable(average, cur,conn):
    cur.execute('DROP TABLE IF EXISTS average')
    cur.execute('CREATE TABLE IF NOT EXISTS average(Artist TEXT PRIMARY KEY, Average REAL)')
    for artist in average:
        cur.execute("INSERT INTO average (Artist, Average) VALUES (?,?)", (artist[0],artist[1]))
    conn.commit()

#compares the top 10 artists that are from deezer that are on the spotify charts with how many average streams they get on Spotify and what their average rank is on Deezer
def setUpComparison(cur,conn):
    cur.execute('DROP TABLE IF EXISTS comparison')
    cur.execute('CREATE TABLE IF NOT EXISTS comparison(Artist TEXT, streams INTEGER)')
    cur.execute('SELECT Top100Songs.name, streams.streams FROM Top100Songs JOIN streams ON Top100Songs.name = streams.artist')
    info = cur.fetchall()
    print(info)
    for artist in info:
        cur.execute("INSERT INTO comparison(Artist, streams) VALUES (?,?)", (artist[0],artist[1]))
    conn.commit()

def barchart_averages():
    label_name = []
    average_streams = []
    for row in average:
        label_name.append(row[0])
    for row2 in average:
        average_streams.append(row2[1])
        
    labels = [label_name[0], label_name[1],label_name[2],label_name[3], label_name[4],label_name[5], label_name[6],label_name[7],label_name[8], label_name[9]]
    avg_streams = [average_streams[0],average_streams[1], average_streams[2],average_streams[3],average_streams[4], average_streams[5], average_streams[6],average_streams[7],average_streams[8], average_streams[9]]
    plt.bar(labels, avg_streams, align = "center", color = ["red", "pink", "lightpink", "green", "deeppink", "navy", "lightblue", "lightgreen","purple","pink"])
    plt.title("Comparison of Average Streams for Artists on the Top 200 Charts")
    plt.ylabel("Average Song Streams (by the millions)")
    plt.xlabel("Artist Name")
    plt.savefig("artist_streams.png")
    plt.show()
    
    return ((label_name[0], average_streams[0]),(label_name[1], average_streams[1]), (label_name[2], average_streams[2]), (label_name[3], average_streams[3]), (label_name[4], average_streams[4]), (label_name[5], average_streams[5]), (label_name[6], average_streams[6]),(label_name[7], average_streams[7]), (label_name[8], average_streams[8]), (label_name[9], average_streams[9]))

def makeScatterplot(info):
    average_rank = []
    average_streams = []
    for row in info:
        average_rank.append(row[1])
    for row2 in info:
        average_streams.append(row2[2])
    plt.scatter(average_rank, average_streams)
    plt.xlabel("Average Rank")
    plt.ylabel("Average Streams")
    plt.title("Average Stream versus Average Rank of top 10 common artists from deezer to spotify")
    plt.savefig("scatterplot.png")
    plt.show()


if __name__ == "__main__":
    info  = find_artist_info()
    cur, conn = setUpDatabase('streams.db')
    setUpSongTable(info, cur, conn)
    average = get_averages(cur,conn)
    #setUpSongTable(info, average, cur, conn)
    setUpAverageTable(average, cur, conn)
    setUpComparison(cur,conn)
    get_averages( cur,conn)
    barchart_averages()
    makeScatterplot(info)
    filename = open("spotifyfile.txt", 'w')
    filename.write("We found the amount of times an artist appeared on the top 200 charts and their total amount of streams on the top 200 charts. Using those two data points, we found each artist's average amount of streams on the top 200 charts and organized it by the top 10.")
    filename.write('\n')
    for elem in barchart_averages():
        filename.write("{} has an average streams of {}".format(elem[0], elem[1]))
        filename.write('\n')
    filename.close()
    