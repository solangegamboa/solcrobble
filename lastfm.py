import os
import pylast
from collections import namedtuple

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "827273248db08020cb101b7971f91d59"  # this is a sample key
API_SECRET = "ee685a5bfdc48ac57cc834cb75122995"

# In order to perform a write operation you need to authenticate yourself
username = "um1up"
password_hash = pylast.md5("guqca7-xuzkyn-dUwhuj")

network = pylast.LastFMNetwork(
    api_key=API_KEY,
    api_secret=API_SECRET,
    username=username,
    password_hash=password_hash,
)

scrobbler_file = "/Volumes/IPOD DE SOL/.scrobbler.log"
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
