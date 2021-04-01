#!/usr/bin/python
# -*- coding: utf-8 -*-
# viewlist.py
# Module of musiclist.py
# Functions that view files in several formats.

import os
import sys
import sqlite3
import csv
import json
import xml.etree.ElementTree as ET
from html.parser import HTMLParser


def encode_decode_screen(unicode_str):
    """
    Convert variable for displaying properly in the screen
    """
    return unicode_str.encode('utf-8').decode(sys.stdout.encoding)


def db_list(db_name):
    """
    Show the content of a SQLite database that contains a Mucic list.
    Table format: artist text, album text, track text
    """
    if os.path.exists(db_name):
        # Connect to DB
        conn = sqlite3.connect(db_name)
        #conn.text_factory = str
        c = conn.cursor()
        c.execute('PRAGMA encoding = "UTF-8";')
        # Get rows of data
        c.execute("SELECT * FROM music")
        rows = c.fetchall()
        for row in rows:
            print(encode_decode_screen(row[0]) + "   |   " +\
                  encode_decode_screen(row[1]) + "   |   " +\
                  encode_decode_screen(row[2]))
        conn.close()
    else:
        print('Database does not exist')

    return


def csv_list(csv_name):
    """
    Show the content of a CSV file that contains a Mucic list.
    CSV format: artist, album, track
    """
    if os.path.exists(csv_name):
        with open(csv_name, 'r', encoding='utf-8') as csvfile:
            spamreader = csv.reader(csvfile)
            for row in spamreader:
                print(encode_decode_screen(row[0]) + ", " +\
                      encode_decode_screen(row[1]) + ", " +\
                      encode_decode_screen(row[2]))
    else:
        print('CSV file does not exist')

    return


def json_list(json_name):
    """
    Show the content of a JSON file that contains a Mucic list.
    Manage 2 kind of JSON formats:
    - Music List
    - Tracks List
    """
    if os.path.exists(json_name):
        with open(json_name, 'r', encoding='utf-8') as json_file:  
            data = json.load(json_file)
            format = data['format']
            if format == 'music-list':
                json_list_music(data)
            elif format == 'tracks-list':
                json_list_tracks(data)
            else:
                print('JSON file does not match a JSON music file')
    else:
        print('JSON file does not exist')

    return


def json_list_music(data):
    """
    Show the content of a JSON file that contains a Mucic list.
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

    music = data['music'][0]
    for i in range(0, len(music['artists'])):
        print('Artist: ', encode_decode_screen(music['artists'][i]['name']))
        for j in range(0, len(music['artists'][i]['albums'])):
            print('  Album: ', encode_decode_screen(music['artists'][i]['albums'][j]['title']))
            for k in range(0, len(music['artists'][i]['albums'][j]['tracks'])):
                print('    Track: ', encode_decode_screen(music['artists'][i]['albums'][j]['tracks'][k]['title']))
        print('')

    return


def json_list_tracks(data):
    """
    Show the content of a JSON (Tracks List) file that contains a Mucic list.
    JSON (Tracks List) format:
      {
          "format": "tracks-list",
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
    for item in data['music']:
        print('Artist: ' + encode_decode_screen(item['artist']))
        print('Album: ' + encode_decode_screen(item['album']))
        print('Track: ' + encode_decode_screen(item['track']))
        print('')

    return


def xml_list(xml_name):
    """
    Show the content of an XML file that contains a Mucic list.
    Manage 2 kind of XML formats:
    - Music List
    - Tracks List
    """
    if os.path.exists(xml_name):
        tree = ET.parse(xml_name)
        #print(tree)
        root = tree.getroot()
        #print(root.tag)
        #print(root.attrib)
        print('Format: ' + root.attrib['format'])
        print('')
        format = root.attrib['format']
        if format == 'music-list':
            xml_list_music(xml_name)
        elif format == 'tracks-list':
            xml_list_tracks(xml_name)
        else:
            print('XML file does not match an XML music file')
    else:
        print('XML file does not exist')

    return


def xml_list_music(xml_name):
    """
    Show the content of an XML (Music List) file that contains a Mucic list.
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
    tree = ET.parse(xml_name)
    root = tree.getroot()
    for artist in root:
        print(artist.tag, ": ", encode_decode_screen(artist.attrib['name']))
        for album in artist:
            print(album.tag, ": ", encode_decode_screen(album.attrib['title']))
            for track in album:
                print(track.tag, ": ", encode_decode_screen(track.text))
            print('')
        print('\n')

    return


def xml_list_tracks(xml_name):
    """
    Show the content of an XML (Tracks List) file that contains a Mucic list.
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

    tree = ET.parse(xml_name)
    root = tree.getroot()
    for item in root:
        for i in item:
            print(i.tag, ": ", encode_decode_screen(i.text))
        print('')

    return


def html_list(html_name):
    """
    Show the content of an HTML file that contains a Mucic list
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
    if os.path.exists(html_name):
        parser = MyHTMLParser()
        f = open(html_name, 'r', encoding='utf-8')
        html= f.read()
        f.close()
        parser.feed(html)
    else:
        print('HTML file does not exist')

    return

class MyHTMLParser(HTMLParser):
    """
    Handle the class HTMLParser
    """
    def handle_starttag(self, tag, attrs):
        # Start tag
        if tag == 'h2':
            print('\nArtist: ', end="")
        if tag == 'h3':
            print('\nAlbum: ', end="")
        if tag == 'li':
            print('Track: ', end="")

    def handle_data(self, data):
        # Data
        if self.get_starttag_text() in ['<h1>', '<h2>', '<h3>', '<li>']:
            print(encode_decode_screen(data))
