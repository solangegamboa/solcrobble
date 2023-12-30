import os
import pylast
from collections import namedtuple

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "API_KEY"  # this is a sample key
API_SECRET = "API_SECRET"

# In order to perform a write operation you need to authenticate yourself
username = "USER"
password_hash = pylast.md5("PASSWORD")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

scrobbler_file = "/Volumes/IPOD/.scrobbler.log"
# with open(scrobbler_file) as f:
#     # contents = f.read()
#     for line in f.readlines(): 
#         if line.startswith("#"):
#             continue
#         print(line)

Record = namedtuple("Record", "artist album title track_number duration rating timestamp mbid")
records = []
with open(scrobbler_file) as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue
        line = line.strip()
        line = line.split('\t')
        line = line[0:8]
        line = Record(*line)
        records.append(line)
    
for records in records:
    scrobbler = network.scrobble(
        artist=records.artist, 
        title=records.title, 
        timestamp=records.timestamp, 
        album=records.album, 
        track_number=records.track_number, 
        duration=records.duration, 
        album_artist=records.artist,
        mbid=records.mbid)

os.remove(scrobbler_file)
