#!/usr/bin/python
# -*- coding: utf-8 -*-
# createlist.py
# Module of musiclist.py
# Functions that create files in several formats.

import os
import sys
import locale
import sqlite3
import csv
import json
import xml.etree.ElementTree as ET

EXT_LIST = ['.MP3', '.M4A']  # List of extensions allowed (in upper case): MP3, ACC
dict_artists = {}            # Music information loaded in memory


def load_music_list(music_dir):
    """
    Load the music list in memory 'dict_artists' from the music directory.

    Example of directory used:
      music/
      │
      ├── artist_1
      │   ├── album_1_1/
      │   │   ├── track_1_1_1
      │   │   ├── track_1_1_2
      │   │   └── track_1_1_3
      │   └── album_1_2/
      │       ├── track_1_2_1
      │       └── track_1_2_2
      ├── artist_2/
      │   ├── album_2_1/
      │   │   ├── track_2_1_1
      │   │   └── track_2_1_2
      │   │
      │   └── album_2_2/
      │       ├── track_2_2_1
      │       └── track_2_2_2
      └── artist_3/
          └── lbum_3_1/
              ├── track_3_1_1
              └── track_3_1_2

    Example of the structure created in memory:
      dict_artists = 
        {'artist-1': {'album-1_1': ['track-1_1_1', 'track-1_1_2', 'track-1_1_3'] ,
                      'album-1_2': ['track-1_2_1', 'track-1_2_2']},
        'artist-2': {'album-2_1': ['track-2_1_1', 'track-2_1_2'],
                      'album-2_2': ['track-2_2_1', 'track-2_2_2']},
        'artist-3': {'album-3_1': ['track-3_1_1', 'track-3_1_2']}
        }
    """

    global dict_artists

    print('Loading music information from "' + music_dir + '"...')
    dict_artists.clear()
    # Artists loop starts, filter only directories
    artists = filter(lambda x: os.path.isdir(os.path.join(music_dir, x)), os.listdir(music_dir))
    for artist in artists:
        dict_albums = {}
        artist_dir = music_dir + os.sep + artist
        # Albums loop starts, filter only directories
        albums = filter(lambda x: os.path.isdir(os.path.join(artist_dir, x)), os.listdir(artist_dir))
        for album in albums:
            album_dir = artist_dir + os.sep + album
            list_tracks = []
            # Tracks loop starts, filter only files
            tracks = filter(lambda x: os.path.isfile(os.path.join(album_dir, x)), os.listdir(album_dir))
            for track in tracks:
                fileext = os.path.splitext(track)[1].upper()
                if fileext in EXT_LIST:
                    list_tracks.append(track)
            # Tracks loop ends    
            dict_albums[album] = list_tracks
            dict_artists[artist] = dict_albums
        # Albums loop ends
    # Artists loop ends
    print('Music information loaded')
    
    return


def write_file(file_name, data):
    """
    Create and write a text file.
    """
    f = open(file_name, 'w', encoding='utf-8')
    for item in data:
        f.write(item + '\n')
    f.close()
    return


def write_json_file(json_name, data):
    """
    Create and write an JSON file.
    """
    with open(json_name, 'w', encoding='utf-8') as json_file:  
        json.dump(data, json_file, indent=2, sort_keys=True)
    return


def write_xml_file(xml_name, data):
    """
    Create and write an XML file.
    """
    tree = ET.ElementTree(data)
    tree.write(xml_name, xml_declaration=True, encoding='utf-8')
    return


def write_html_file(html_name, data):
    """
    Create and write an HTML file.
    """
    with open(html_name, 'wb') as f:
        f.write('<!doctype html>'.encode('utf8'))
        tree = ET.ElementTree(data)
        tree.write(f, 'utf-8')
    return


def print_list():
    """
    Show in the screen the content of the Mucic list in 'dict_artists'.
    """
    global dict_artists

    print('\nMUSIC LIST')
    print('----------')
    for k_artist in sorted(dict_artists.keys()):
        for  k_album in sorted(dict_artists[k_artist].keys()):
            print('ARTIST: ', k_artist.encode('utf-8').decode(sys.stdout.encoding))
            print('ALBUM: ', k_album.encode('utf-8').decode(sys.stdout.encoding))
            print('TRACKS:')
            for track in sorted(dict_artists[k_artist][k_album]):
                print('    ', track.encode('utf-8').decode(sys.stdout.encoding))
            print('')

    return


def file_list(file_name):
    """
    Create a text file with the content of the Mucic list in 'dict_artists'.
    """
    global dict_artists
    output = []

    print('Creating file "' + file_name + '"...')
    output.append("MUSIC LIST")
    output.append('----------\n')
    for k_artist in sorted(dict_artists.keys()):
        for  k_album in sorted(dict_artists[k_artist].keys()):
            output.append('ARTIST: ' + k_artist)
            output.append('ALBUM: ' + k_album)
            output.append('TRACKS:')
            for track in sorted(dict_artists[k_artist][k_album]):
                output.append("        " + track)
            output.append("")

    write_file(file_name, output)
    print('File created')

    return


def db_list(db_name):
    """
    Create a SQLite database with the content of the Mucic list in 'dict_artists'.
    Table format: artist text, album text, track text
    """
    global dict_artists

    print('Creating Database "' + db_name + '"...')
    
    # if DB exists then remove 
    if os.path.exists(db_name):
        os.remove(db_name)

    # Create and connect to DB
    conn = sqlite3.connect(db_name)
    #conn.text_factory = str
    
    c = conn.cursor()
    c.execute('PRAGMA encoding = "UTF-8";')
    
    # Create table
    c.execute('''CREATE TABLE music
              (artist text, album text, track text)''')

    # Create index
    c.execute('''CREATE INDEX idx_music
                ON music (artist, album)''')

    # Insert rows of data
    for k_artist in sorted(dict_artists.keys()):
        for  k_album in sorted(dict_artists[k_artist].keys()):
            for track in sorted(dict_artists[k_artist][k_album]):
                row = [k_artist, k_album, track]
                c.execute("INSERT INTO music VALUES (?, ?, ?)", row)
    
    # Save (commit) the changes
    conn.commit()
              
    conn.close()
    print('Database created')
      
    return


def csv_list(csv_name):
    """
    Create a CSV file with the content of the Mucic list in 'dict_artists'.
    CSV format: artist, album, track
    """
    global dict_artists

    print('Creating CSV file "' + csv_name + '"...')
    with open(csv_name, 'w', encoding='utf-8', newline='') as csvfile:
        spamwriter = csv.writer(csvfile)
        for k_artist in sorted(dict_artists.keys()):
            for  k_album in sorted(dict_artists[k_artist].keys()):
                for track in sorted(dict_artists[k_artist][k_album]):
                    spamwriter.writerow([k_artist, k_album, track])
    print('CSV file created')

    return


def json_list_music(json_name):
    """
    Create a JSON (Music List) file with the content of the Mucic list in 'dict_artists'.
    JSON (Music List) format:
      {
          "format": "music-list",
          "music": [
              {
                  "artists": [
                      {
                          "name": "author-1",
                          "albums": [ 
                              {
                                  "title": "album-1_1",
                                  "tracks": [
                                      {
                                          "title": "track_1_1_1",
                                          "title": "track_1_1_2"
                                      }
                                  ]
                              }
                          ]
                      }
                  ]
              }
          ]
      }
    """
    global dict_artists

    print('Creating JSON (Music List) file "' + json_name + '"...')
    data = {}
    data['format'] = "music-list"
    data['music'] = []

    artists = {}
    artists['artists'] = []
    for k_artist in sorted(dict_artists.keys()):
        albums = {}
        albums['albums'] = []
        for  k_album in sorted(dict_artists[k_artist].keys()):
            tracks = {}
            tracks['tracks'] = []
            for track in sorted(dict_artists[k_artist][k_album]):
                tracks['tracks'].append({'title': track})
            albums['albums'].append({'title': k_album, 'tracks': tracks['tracks']})
        artists['artists'].append({'name': k_artist, 'albums': albums['albums']})
        data['music'].append({'artists': artists['artists']})

    write_json_file(json_name, data)
    print('JSON (Music List) file created')

    return


def json_list_tracks(json_name):
    """
    Create a JSON (Tracks List) file with the content of the Mucic list in 'dict_artists'.
    JSON (Tracks List) format:
      {
          "format": "tracks-list"
          "music": [
              {
                  "artist": "author-1",
                  "album": "album-1_1",
                  "tracks": "track_1_1_1"
              },
              {
                  "artist": "author-1",
                  "album": "album-1_1",
                  "tracks": "track_1_1_2"
              }
          ]
      }
    """
    global dict_artists

    print('Creating JSON (Tracks List) file "' + json_name + '"...')
    data = {}
    data['format'] = "tracks-list"
    data['music'] = []  
    for k_artist in sorted(dict_artists.keys()):
        for  k_album in sorted(dict_artists[k_artist].keys()):
            for track in sorted(dict_artists[k_artist][k_album]):
                data['music'].append({  
                    'artist': k_artist,
                    'album': k_album,
                    'track': track})

    write_json_file(json_name, data)
    print('JSON (Tracks List) file created')

    return


def xml_list_music(xml_name):
    """
    Create a XML (Music List) file with the content of the Mucic list in 'dict_artists'.
    XML (Music List) format:
      <music format="music-list">
          <artist name="author-1">
              <album title="album-1_1">
                  <track>track_1_1_1</track>
                  <track>track_1_1_2</track>
              </album>
          </artist>
      </music>
    """
    global dict_artists

    print('Creating (Music List) XML file "' + xml_name + '"...')
    music = ET.Element("music", {'format': 'music-list'})
    for k_artist in sorted(dict_artists.keys()):
        artist = ET.SubElement(music, "artist", {'name': k_artist})
        for  k_album in sorted(dict_artists[k_artist].keys()):
            album = ET.SubElement(artist, "album", {'title': k_album})
            for track in sorted(dict_artists[k_artist][k_album]):
                ET.SubElement(album, "track").text = track

    write_xml_file(xml_name, music)
    print('XML (Music List) file created')

    return


def xml_list_tracks(xml_name):
    """
    Create a XML (Tracks List) file with the content of the Mucic list in 'dict_artists'.
    XML (Tracks List) format:
      <music format="tracks-list">
          <item>
              <artist>"author-1"</artist>
              <album>"album-1_1"</album>
              <track>"track_1_1_1"</track>
          </item>
          <item>
              <artist>"author-1"</artist>
              <album>"album-1_1"</album>
              <track>"track_1_1_2"</track>
          </item>
      </music>
    """
    global dict_artists

    print('Creating XML (Tracks List) file "' + xml_name + '"...')
    music = ET.Element("music", {'format': 'tracks-list'})
    for k_artist in sorted(dict_artists.keys()):
        for  k_album in sorted(dict_artists[k_artist].keys()):
            for track in sorted(dict_artists[k_artist][k_album]):
                item = ET.SubElement(music, "item")
                ET.SubElement(item, "artist").text = k_artist
                ET.SubElement(item, "album").text = k_album
                ET.SubElement(item, "track").text = track

    write_xml_file(xml_name, music)
    print('XML (Tracks List) file created')

    return


def html_list(html_name):
    """
    Create a HTML file with the content of the Mucic list in 'dict_artists'.
    HTML format:
      <html>
      <head>
          <title>MUSIC</title>
      </head>
      <body>
          <h1>MUSIC LIST</h1>
          <h2>author-1<h2>
          <h3>album-1_1<h2>
          <ul>
              <li>track_1_1_1</li>
              <li>track_1_1_2</li>
          <ul>
      </body>
      </html>
    """
    global dict_artists

    print('Creating HTML file "' + html_name + '"...')
    page = ET.Element('html')
    head = ET.SubElement(page, 'head')
    ET.SubElement(head, 'meta', {'charset': "UTF-8"})
    ET.SubElement(head, 'title').text = 'MUSIC LIST'
    body = ET.SubElement(page, 'body')
    ET.SubElement(body, 'h1').text = 'MUSIC LIST'
    
    for k_artist in sorted(dict_artists.keys()):
        ET.SubElement(body, 'h2').text = k_artist
        for  k_album in sorted(dict_artists[k_artist].keys()):
            ET.SubElement(body, 'h3').text = k_album
            ul = ET.SubElement(body, 'ul')
            for track in sorted(dict_artists[k_artist][k_album]):
                ET.SubElement(ul, "li").text = track
    
    write_html_file(html_name, page)
    print('HTML file created')

    return
