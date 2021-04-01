#!/usr/bin/python
# -*- coding: utf-8 -*-
# musiclist.py
# Main application of musiclist tool.
# This utility allows to read a music structure in your file system,
# and create a file with the information in several formats.

import os
import sys
import argparse
from musicmod import createlist
from musicmod import viewlist


def is_dir(string):
    if not string:  # Not directory parameter
        return os.getcwd()
    else:
        if os.path.isdir(string):
            return string
        else:
            print('Error, directory \''  + string + '\' does not exist')
            sys.exit(1)
    return


def main():
    # Make a list of command line arguments, omitting the [0] element
    # which is the script itself.
    args = sys.argv[1:]
    if not args:
        print('\nusage: musiclist.py [-h] [--path MUSIC_DIR] [-p]\n' + \
              '                    [-f FILE_NAME] [-d DB_NAME] [-c CSV_NAME]\n' + \
              '                    [-j JSON_NAME] [-j2 JSON_NAME]\n' + \
              '                    [-x XML_NAME] [-x2 XML_NAME]\n' + \
              '                    [--html HTML_NAME]\n' + \
              '                    [--dbview DB_VIEW] [--csvview CSV_VIEW]\n' + \
              '                    [--jsonview JSON_VIEW] [--xmlview XML_VIEW]' + \
              '                    [--htmlview HTML_VIEW]')
    else:
        parser = argparse.ArgumentParser(description='Manage music list')
        parser.add_argument('--path', type=is_dir, action='store', default='', dest="music_dir", help='directory where the music is')
        parser.add_argument('-p', '--print', action='store_true', default=False, dest='printlist', help='print music list')
        parser.add_argument('-f', '--file', action='store', dest="file_name", help='write music list to a text file')
        parser.add_argument('-d', '--db', action='store', dest="db_name", help='write music list to SQLite Database')
        parser.add_argument('-c', '--csv', action='store', dest="csv_name", help='write music list to a CSV file')
        parser.add_argument('-j', '--json', action='store', dest="json_name", help='write music list (music list) to a JSON file')
        parser.add_argument('-j2', '--json2', action='store', dest="json_name2", help='write music list (tracks list) to a JSON file')
        parser.add_argument('-x', '--xml', action='store', dest="xml_name", help='write music list (music list) to an XML file')
        parser.add_argument('-x2', '--xml2', action='store', dest="xml_name2", help='write music list (tracks list) to an XML file')
        parser.add_argument('--html', action='store', dest="html_name", help='write music list to an HTML file')
        parser.add_argument('--dbview', action='store', dest="db_view", help='view music list from a SQLite Database')
        parser.add_argument('--csvview', action='store', dest="csv_view", help='view music list from a CSV file')
        parser.add_argument('--jsonview', action='store', dest="json_view", help='view music list from a JSON file')
        parser.add_argument('--xmlview', action='store', dest="xml_view", help='view music list from an XML file')
        parser.add_argument('--htmlview', action='store', dest="html_view", help='view music list from an HTML file')

        args = parser.parse_args()

        # Load music information from the directory
        if args.printlist or args.file_name  or args.db_name or args.csv_name or \
              args.json_name or args.json_name2 or \
              args.xml_name or args.xml_name2 or \
              args.html_name:
            createlist.load_music_list(args.music_dir)

        # Execute options
        if args.printlist:
            createlist.print_list()
        if args.file_name:
            createlist.file_list(args.file_name)
        if args.db_name:
            createlist.db_list(args.db_name)
        if args.csv_name:
            createlist.csv_list(args.csv_name)
        if args.json_name:
            createlist.json_list_music(args.json_name)
        if args.json_name2:
            createlist.json_list_tracks(args.json_name2)
        if args.xml_name:
            createlist.xml_list_music(args.xml_name)
        if args.xml_name2:
            createlist.xml_list_tracks(args.xml_name2)
        if args.html_name:
            createlist.html_list(args.html_name)
        if args.db_view:
            viewlist.db_list(args.db_view)
        if args.csv_view:
            viewlist.csv_list(args.csv_view)
        if args.json_view:
            viewlist.json_list(args.json_view)
        if args.xml_view:
            viewlist.xml_list(args.xml_view)
        if args.html_view:
            viewlist.html_list(args.html_view)

    return


# This is the standard boilerplate that calls the main() function.
if __name__ == '__main__':
    main()
