# Music parser


## Console output
 1. install MongoDB, if not installed
 2. start MongoDB service
 3. install python and pip
 4. install requirements `pip install requirements.txt`
 5. Start `manage.py` file with terminal `python manage.py command [args]`

##### Commands:
 * `help` - write help info
 * `search [args]` - send "search query in quotation marks" as args
 * `export [args]` - send 1/0 - dump media files or not 
 
## Class functional

### How to start
 * Create SearchEngine object
 * Call start method with search query
 * SearchEngine will connect to MongoDB
 * MongoDB database with name `music_search` will contain all find info
 
 ##### Database Tables
 * `music_search.artist` - info about artists
 * `music_search.song` - info about songs
 * `music_search.log` - logs


### Methods
 * `start` - start parse site with search request
 * `len` - number of artist found
 * `write_json` - dump database to json file
 * `to_json` - dump database to json (return array of artist and song database in json)
 * `_get_artist_info` - get info about the artist, if there is no artist in the database, then create a new
 
 
### Models

 #### Artist
  * `name` - artist name
  * `image` - artist image(from song)
  * `created_at` - time when artist was added 
  
 #### Song
  * `artist` - artist id
  * `name` - song name
  * `duration` - song duration
  * `size` - song size
  * `download_url` - url for download song
  * `audio_file` - song audio file
  * `created_at` - time when song was added 

 #### Log
  * `type_added` - type of added model (song/artist)
  * `name_added` - added model name
  * `created_at` - time when log was added 
  * `added` - item was added or error

  
### DB Methods
 * `add_artists` - add many artists
 * `add_artist` - add one artist
 * `add_tracklist` - add track list (>1 song)
 * `add_song` - add one song
 * `get_artist_tracklist` - get track list of artist with name
 * `get_artist_by_song` - get song artist
 * `get_artist` - get artist by name
 * `is_artist_exist` - check artist in database
 * `show_all_artist` - return all artist in database
 * `to_json_artist` - dump artist database to json 
 * `to_json_song` - dump song database to json 
 * `download` - download file from url to temp file
