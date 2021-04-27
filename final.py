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


result = requests.get('https://api.deezer.com/playlist/1313621735/tracks')
d = result.json()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpSongsTable(tracks, cur, conn):
    cur.execute('DROP TABLE IF EXISTS Top100Songs')
    cur.execute('CREATE TABLE IF NOT EXISTS Top100Songs (song_id INTEGER, title TEXT UNIQUE, name TEXT, album TEXT, duration INTEGER, rank INTEGER)')
    for song in tracks['data']:
        song_id = song['id']
        title = song['title']
        name= song['artist']['name']
        album = song['album']['title']
        duration = song['duration']
        rank = song['rank']
        cur.execute('INSERT OR IGNORE INTO Top100Songs (song_id, title, name, album, duration, rank) VALUES(?, ?, ?, ?, ?, ?)', (song_id, title, name, album, duration, rank))
        conn.commit()



def findArtistTopSongsCount(tracks, cur, conn):
    artist_list = []
    for song in tracks['data']: 
        artist = song['artist']['name']
        artist_list.append(artist)
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
    plt.title("Number of Songs for Top 10 Artists on the Top 25 Charts")
    plt.ylabel("Songs in the Top 25 Charts")
    plt.xlabel("Artist Name")
    plt.savefig("artist_counts.png")
    plt.show()
    
    return((labels_list[0], song_counts[0]), (labels_list[1], song_counts[1]), (labels_list[2], song_counts[2]), (labels_list[3], song_counts[3]), (labels_list[4], song_counts[4]), (labels_list[5], song_counts[5]), (labels_list[6], song_counts[6]), (labels_list[7], song_counts[7]), (labels_list[8], song_counts[8]), (labels_list[9], song_counts[9]))

def findAverageRank(tracks, cur, conn):
    ranks = []
    for song in tracks['data']: 
        artist = song['artist']['name']
        rank = song['rank']
        ranks.append((artist, rank))
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

def createBarGraph2(tuple_list):
    labels_list = []
    ranks_average = []
    for item in tuple_list:
        labels_list.append(item[0]), ranks_average.append(item[1])

    labels = [labels_list[0], labels_list[1], labels_list[2], labels_list[3], labels_list[4], labels_list[5], labels_list[6], labels_list[7], labels_list[8], labels_list[9]]
    ranking = [ranks_average[0], ranks_average[1], ranks_average[2], ranks_average[3], ranks_average[4], ranks_average[5], ranks_average[6], ranks_average[7], ranks_average[8], ranks_average[9]]
    plt.bar(labels, ranking, align = "center", color = ["red", "pink", "lightpink", "green", "deeppink", "navy", "lightblue", "lightgreen","purple","pink"])
    plt.title("Average Rank of Songs in the Top 25 for Artists")
    plt.ylabel("Average Ranks of Songs out of 1 million")
    plt.xlabel("Artist Name")
    plt.savefig("artist_ranks.png")
    plt.show()

    return((labels_list[0], ranks_average[0]), (labels_list[1], ranks_average[1]), (labels_list[2], ranks_average[2]), (labels_list[3], ranks_average[3]), (labels_list[4], ranks_average[4]), (labels_list[5], ranks_average[5]), (labels_list[6], ranks_average[6]), (labels_list[7], ranks_average[7]), (labels_list[8], ranks_average[8]), (labels_list[9], ranks_average[9]))


def main():
    data = d
    cur, conn = setUpDatabase('streams.db')
    setUpSongsTable(data, cur, conn)

    sorted_dict = findArtistTopSongsCount(data, cur, conn)
    createBarGraph(sorted_dict)
    ranks = findAverageRank(data, cur, conn)
    createBarGraph2(ranks)

if __name__ == "__main__":
    main()
