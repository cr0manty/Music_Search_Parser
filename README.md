# Music parser

 ## Console output
1. install python and pip
2. install requirements `pip install requirements.txt`
3. Start `main.py` file with command line or terminal `python main.py`
4. select menu item and wait
 
## Class functional

### How to start
* Create SearchEngine object
* Call start method with search query
*  SearchEngine `content` will store all the results found 

### Methods

 * `len` - number of results found
 * `import_from_json` - update database from json file
 * `write_json` - dump database to json file
 * `to_json` - dump database to json
 * `update_content` - update database with 1 object 
 * `check_content` - check object for database format
 * `check_artist` - check the artist name and return index of artist in database, if the artist is not in the database, then returns `-1`
 * `_get_artist_info` - get info about the artist, if there is no artist in the database, then create a new
 * `_try_get_list` - for loop for `get_artist_info`
 
