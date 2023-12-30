import pylast
import os
from collections import namedtuple

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from https://www.last.fm/api/account/create for Last.fm
API_KEY = "827273248db08020cb101b7971f91d59"  # this is a sample key
API_SECRET = "ee685a5bfdc48ac57cc834cb75122995"

SESSION_KEY_FILE = os.path.join(os.path.expanduser("~"), ".session_key")
network = pylast.LastFMNetwork(API_KEY, API_SECRET)
if not os.path.exists(SESSION_KEY_FILE):
    skg = pylast.SessionKeyGenerator(network)
    url = skg.get_web_auth_url()

    print(f"Please authorize this script to access your account: {url}\n")
    import time
    import webbrowser

    webbrowser.open(url)

    while True:
        try:
            session_key = skg.get_web_auth_session_key(url)
            with open(SESSION_KEY_FILE, "w") as f:
                f.write(session_key)
            break
        except pylast.WSError:
            time.sleep(1)
else:
    session_key = open(SESSION_KEY_FILE).read()

network.session_key = session_key

scrobbler_file = "/Volumes/IPOD DE SOL/.scrobbler.log"

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
 
multiscroble = []   
for records in records:
    scrobbler = {
                    "artist": records.artist,
                    "title": records.title,
                    "timestamp": records.timestamp,
                    "album": records.album,
                    "album_artist": records.artist,
                    "track_number": records.track_number,
                    "duration": records.duration,
                    "mbid": records.mbid,
                }
    multiscroble.append(scrobbler)

network.scrobble_many(multiscroble)

os.remove(scrobbler_file)
