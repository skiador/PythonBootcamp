import datetime
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

SPOTIPY_CLIENT_ID = os.environ["SPOTIPY_CLIENT_ID"]
SPOTIPY_CLIENT_SECRET = os.environ["SPOTIPY_CLIENT_SECRET"]
SPOTIPY_REDIRECT_URL = "https://example.org"

# Ask user for date
date_format = "%d/%m/%Y"
while True:
    try:
        date = datetime.datetime.strptime(input("Enter the desired date (dd/mm/yyyy): "), date_format)
        break
    except ValueError:
        print("Enter a valid date. Try again.")


formatted_date = datetime.date.strftime(date, "%Y-%m-%d")

# Request data from website
url = f"https://www.billboard.com/charts/hot-100/{formatted_date}"
connection = requests.get(url)
html_text = connection.text
soup = BeautifulSoup(html_text, "html.parser")

song_containers = soup.find_all("div", class_="o-chart-results-list-row-container")

song_dict = {index+1: item.find_next(id="title-of-a-story").text.strip() for index, item in enumerate(song_containers)}
if len(song_dict) == 100:
    print("Songs obtained correctly")
else:
    raise Exception("Error while obtaining all songs")

# Spotify API
scope = "playlist-modify-private"
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=SPOTIPY_CLIENT_ID,
        client_secret=SPOTIPY_CLIENT_SECRET,
        redirect_uri=SPOTIPY_REDIRECT_URL,
        scope=scope
    )
)
user_id = sp.me()["id"]
print("Successfully connected to user account")

# Create playlist
name = f"100 Billboard {formatted_date}"
new_playlist = sp.user_playlist_create(user=user_id, name=name, public=False)
playlist_id = new_playlist["id"]
print("New playlist created")

# Retrieve songs id
print("Retrieving songs info...")
songs_uri = [sp.search(song, limit=1, type="track")["tracks"]["items"][0]["uri"] for song in list(song_dict.values())]

# Add songs
print("Adding songs...")
sp.playlist_add_items(playlist_id=playlist_id, items=songs_uri)
print("ALL SONGS ADDED!")
