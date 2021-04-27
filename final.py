#Final Project - Andie Carroll

import unittest
import sqlite3
import json
import os
import requests
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


result = requests.get('https://api.deezer.com/playlist/1313621735/tracks')
d = result.json()

def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def setUpSongsTable(tracks, cur, conn):
    cur.execute('CREATE TABLE IF NOT EXISTS Top100Songs (song_id INTEGER, title TEXT UNIQUE, artist TEXT, album TEXT, duration INTEGER)')
    for song in tracks['data']:
        song_id = song['id']
        title = song['title']
        artist = song['artist']['name']
        album = song['album']['title']
        duration = song['duration']
        cur.execute('INSERT OR IGNORE INTO Top100Songs (song_id, title, artist, album, duration) VALUES(?, ?, ?, ?, ?)', (song_id, title, artist, album, duration))
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

    labels = [labels_list[0], labels_list[1], labels_list[2], labels_list[3], labels_list[4], labels_list[5], labels_list[6], labels_list[7], labels_list[8], labels_list[9], labels_list[10], labels_list[11], labels_list[12], labels_list[13], labels_list[14], labels_list[15], labels_list[16], labels_list[17], labels_list[18], labels_list[19]]
    counting = [song_counts[0], song_counts[1], song_counts[2], song_counts[3], song_counts[4], song_counts[5], song_counts[6], song_counts[7], song_counts[8], song_counts[9], song_counts[10], song_counts[11], song_counts[12],song_counts[13], song_counts[14], song_counts[15],song_counts[16], song_counts[17], song_counts[18],song_counts[19]]
    plt.bar(labels, counting, align = "center")
    plt.title("Number of Songs for Artists on the Top 25 Charts")
    plt.ylabel("Song in the Top 25 Charts")
    plt.xlabel("Artist Name")
    plt.savefig("artist_counts.png")
    plt.show()
    
    return((labels_list[0], song_counts[0]), (labels_list[1], song_counts[1]), (labels_list[2], song_counts[2]), (labels_list[3], song_counts[3]), (labels_list[4], song_counts[4]), (labels_list[5], song_counts[5]), (labels_list[6], song_counts[6]), (labels_list[7], song_counts[7]), (labels_list[8], song_counts[8]), (labels_list[9], song_counts[9]), (labels_list[10], song_counts[10]), (labels_list[11], song_counts[11]), (labels_list[12], song_counts[12]), (labels_list[13], song_counts[13]), (labels_list[14], song_counts[14]), (labels_list[15], song_counts[15]), (labels_list[16], song_counts[16]), (labels_list[17], song_counts[17]), (labels_list[18], song_counts[18]), (labels_list[19], song_counts[19]))



#def findAverageDuration(cur, conn):
    #cur.execute('SELECT AVG(duration) FROM Top100Songs').fetchall()

def main():
    data = d
    cur, conn = setUpDatabase('charts.db')
    setUpSongsTable(data, cur, conn)
    sorted_dict = findArtistTopSongsCount(data, cur, conn)
    createBarGraph(sorted_dict)

if __name__ == "__main__":
    main()
