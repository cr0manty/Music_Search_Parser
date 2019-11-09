# Music parser

## Console output
 1. install MongoDB, if not installed
 2. start MongoDB service
 3. install python and pip
 4. install requirements `pip install requirements.txt`
 5. Start `main.py` file with command line or terminal `python main.py`
 6. select menu item and wait
 
## Class functional

### How to start
 * Create SearchEngine object
 * Call start method with search query
 * SearchEngine will connect to MongoDB
 * MongoDB database with name `music_search` will contain all find info
 * `music_search.artist` - info about artists
 * `music_search.song` - info about songs

### Methods
 * `start` - start parse site with search request
 * `len` - number of artist found
 * `write_json` - dump database to json file
 * `to_json` - dump database to json (return array of artist and song database in json)
 * `_get_artist_info` - get info about the artist, if there is no artist in the database, then create a new
 
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
