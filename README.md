# Music List utility in Python

This repo contains a Music List utility in Python code.

This utility allows to read a music structure in your file system, and create a file with the information in several formats:

* Plain Text
* SQLite Database
* CVS
* JSON (Music List format)
* JSON (Tracks List format)
* XML (Music List format)
* XML (Tracks List format)
* HTML

## Requirements

* The code was written for Python 3.

## Using the utility

This utility allows to read a music structure in your file system:

```bash
music/
│
├── artist_1
│   ├── album_1_1/
│   │   ├── track_1_1_1
│   │   ├── track_1_1_2
│   │   └── track_1_1_3
│   │
│   └── album_1_2/
│       ├── track_1_2_1
│       └── track_1_2_2
│ 
├── artist_2/
│   ├── album_2_1/
│   │   ├── track_2_1_1
│   │   └── track_2_1_2
│   │
│   └── album_2_2/
│       ├── track_2_2_1
│       └── track_2_2_2
│
└── artist_3/
    └── lbum_3_1/
        ├── track_3_1_1
        └── track_3_1_2
```

Run the utility:

```bash
python musiclist.py <parameters>
```

Parameters:

```bash
--path          directory where the music is
-p  --print     print music list
-f  --file      write music list to a text file
-d  --db        write music list to SQLite Database
-c  --csv       write music list to a CSV file
-j  --json      write music list (music list) to a JSON file
-j2 --json2     write music list (tracks list) to a JSON file
-x  --xml       write music list (music list) to an XML file
-x2 --xml2      write music list (tracks list) to an XML file
-h  --html      write music list to an HTML file
--dbview        view music list information from a SQLite Database
--csvview       view music list information from a CSV file
--jsonview      view music list information from a JSON file
--xmlview       view music list information from an XML file
--htmlview      view music list information from an HTML file
```


## Using the code

* The application has this components:

  ```bash
  musiclist.py
  musicmod/
  ├── __init__.py
  ├── createlist.py
  └── viewlist.py
  ```

  * `musiclist.py`: Main application that manages the parameters in the command line and calls the functions.
  * `__init__.py`: It contains the definition of the `musicmod` directory as a package.
  * `createlist.py`: It contains the funtion that read the music directory and all funtions that create the format files.
  * `viewlist.py`: It contains the functions that view the content of the format files.

* When the utility is run with a paramenter for creating a file:
  
  1. Read the music directory.

     Example of directory:

     ```bash
     music/
     │
     ├── artist_1
     │   ├── album_1_1/
     │   │   ├── track_1_1_1
     │   │   ├── track_1_1_2
     │   │   └── track_1_1_3
     │   │
     │   └── album_1_2/
     │       ├── track_1_2_1
     │       └── track_1_2_2
     │ 
     ├── artist_2/
     │   ├── album_2_1/
     │   │   ├── track_2_1_1
     │   │   └── track_2_1_2
     │   │
     │   └── album_2_2/
     │       ├── track_2_2_1
     │       └── track_2_2_2
     │
     └── artist_3/
         └── lbum_3_1/
             ├── track_3_1_1
             └── track_3_1_2
     ```
  2. Load the music list in memory `dict_artists`.

     Example of structure used:

     ```bash
     dict_artists = 
     {'artist-1': {'album-1_1': ['track-1_1_1', 'track-1_1_2', 'track-1_1_3'],
                   'album-1_2': ['track-1_2_1', 'track-1_2_2']},
      'artist-2': {'album-2_1': ['track-2_1_1', 'track-2_1_2'],
                   'album-2_2': ['track-2_2_1', 'track-2_2_2']},
      'artist-3': {'album-3_1': ['track-3_1_1', 'track-3_1_2']}
     }
     ```

  3. Save the music list information in a file in the format selected.

* When the utility is run with a paramenter for view a file:
  
  1. Read the file.
  2. Parse the format (Plain Text, SQLite Database, CSV, JSON, XML, HTML).
  3. Show the music list information on the screen.

* The utility uses differents formats for storing the information:
  
  * Plain Text
  
  * SQLite Database
    
    Table format: artist text, album text, track text

  * CVS
  
    Format: artist, album, track

  * JSON in Music List format
  
    ```json
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
    ```

  * JSON in Tracks List format

    ```json
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

    ```

  * XML in Music List format

    ```xml
    <music format="music-list">
        <artist name="author-1">
            <album title="album-1_1">
                <track>track_1_1_1</track>
                <track>track_1_1_2</track>
            </album>
        </artist>
    </music>
    ```

  * XML in Tracks List format

    ```xml
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

    ```

  * HTML

    ```html
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
  
    ```

  
## License

This code is released under the MIT License. See LICENSE file.