#Final Project - Andie Carroll

import unittest
import sqlite3
import json
import os
import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


result = requests.get('https://api.deezer.com/playlist/1313621735')
d = result.json()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpSongsTable(tracks, cur, conn):
    cur.execute('DROP TABLE IF EXISTS Top100Songs')
    cur.execute('CREATE TABLE IF NOT EXISTS Top100Songs (title TEXT PRIMARY KEY, artist text, album TEXT, duration INTEGER, rank INTEGER)')
    for song in tracks['tracks']['data']:
        title = song['title']
        artist = song['artist']['name']
        album = song['album']['title']
        duration = song['duration']
        rank = song['rank']
        cur.execute('INSERT OR IGNORE INTO Top100Songs (title, artist, album, duration, rank) VALUES(?, ?, ?, ?, ?)', (title, artist, album, duration, rank))
        conn.commit()

def findArtistTopSongsCount(cur, conn):
    cur.execute('SELECT artist FROM Top100Songs')
    result = cur.fetchall()
    print(result)
    artist_list = []
    for artist in result: 
        artist_list.append(artist[0])
    counts = {}
    for artist in artist_list:
        counts[artist] = counts.get(artist, 0) + 1
    sorted_artists = sorted(counts.items(), key=lambda x:x[1], reverse = True)
    print(sorted_artists)
    return(sorted_artists)

def createBarGraph(tuple_list):
    labels_list = []
    song_counts = []
    for item in tuple_list:
        labels_list.append(item[0]), song_counts.append(item[1])

    labels = [labels_list[0], labels_list[1], labels_list[2], labels_list[3], labels_list[4], labels_list[5], labels_list[6], labels_list[7], labels_list[8], labels_list[9]]
    counting = [song_counts[0], song_counts[1], song_counts[2], song_counts[3], song_counts[4], song_counts[5], song_counts[6], song_counts[7], song_counts[8], song_counts[9]]
    plt.bar(labels, counting, align = "center")
    plt.title("Number of Songs for Artists on the Top 100 Chart")
    plt.ylabel("Songs in the Top 100 Charts")
    plt.xlabel("Artist Name")
    plt.savefig("artist_counts.png")
    plt.show()
    
    return((labels_list[0], song_counts[0]), (labels_list[1], song_counts[1]), (labels_list[2], song_counts[2]), (labels_list[3], song_counts[3]), (labels_list[4], song_counts[4]), (labels_list[5], song_counts[5]), (labels_list[6], song_counts[6]), (labels_list[7], song_counts[7]), (labels_list[8], song_counts[8]), (labels_list[9], song_counts[9]))

def findAverageRank(cur, conn):
    cur.execute('SELECT artist, rank FROM Top100Songs')
    ranks = cur.fetchall()
    print(ranks)
    d = defaultdict(list)
    for k, v in ranks:
        d[k].append(v)
    print(d)
    average_ranks = []
    for k, v in d.items():
        artist = k
        adds = 0
        length = len(v)
        for y in v:
            adds += y
        average = adds/length
        average_ranks.append((artist, average))
    sorted_averages = sorted(average_ranks, key=lambda x:x[1], reverse = True)
    print(sorted_averages)
    return sorted_averages

def setUpAverageTable(ranks, cur,conn):
    cur.execute('DROP TABLE IF EXISTS average_ranks')
    cur.execute('CREATE TABLE IF NOT EXISTS average_ranks(Artist TEXT PRIMARY KEY, Average REAL)')
    for artist in ranks:
        cur.execute("INSERT INTO average_ranks (Artist, Average) VALUES (?,?)", (artist[0],artist[1]))
    conn.commit()

def createBarGraph2(tuple_list):
    labels_list = []
    ranks_average = []
    for item in tuple_list:
        labels_list.append(item[0]), ranks_average.append(item[1])

    labels = [labels_list[0], labels_list[1], labels_list[2], labels_list[3], labels_list[4], labels_list[5], labels_list[6], labels_list[7], labels_list[8], labels_list[9]]
    ranking = [ranks_average[0], ranks_average[1], ranks_average[2], ranks_average[3], ranks_average[4], ranks_average[5], ranks_average[6], ranks_average[7], ranks_average[8], ranks_average[9]]
    plt.bar(labels, ranking, align = "center", color = ["red", "pink", "lightpink", "green", "deeppink", "navy", "lightblue", "lightgreen","purple","pink"])
    plt.title("Average Rank of Songs in the Top 100 for Artists")
    plt.ylabel("Average Ranks of Songs out of 1 million")
    plt.xlabel("Artist Name")
    plt.savefig("artist_ranks.png")
    plt.show()

    return((labels_list[0], ranks_average[0]), (labels_list[1], ranks_average[1]), (labels_list[2], ranks_average[2]), (labels_list[3], ranks_average[3]), (labels_list[4], ranks_average[4]), (labels_list[5], ranks_average[5]), (labels_list[6], ranks_average[6]), (labels_list[7], ranks_average[7]), (labels_list[8], ranks_average[8]), (labels_list[9], ranks_average[9]))


def main():
    data = d
    cur, conn = setUpDatabase('streams.db')
    setUpSongsTable(data, cur, conn)
    sorted_dict = findArtistTopSongsCount(cur, conn)
    createBarGraph(sorted_dict)
    ranks = findAverageRank(cur, conn)
    setUpAverageTable(ranks, cur,conn)
    createBarGraph2(ranks)
    filename = open('deezerfile.txt', 'w')
    filename.write("We found the amount of times an artist appeared in the top 100 charts for the US and the average rank of their songs in the top 100 charts for the US")
    filename.write('\n')
    for elem in findArtistTopSongsCount(cur, conn):
        filename.write('{} has {} song(s) in the top 100 charts'.format(elem[0], elem[1]))
        filename.write('\n')
    filename.close()

if __name__ == "__main__":
    main()
