import os
import requests
from dotenv import load_dotenv
import datetime
import base64
import json
from youtube_search import YoutubeSearch

client_id = os.getenv("ID")
client_secret = os.getenv("SECRET")

client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": "client_credentials"
}
token_headers = {
    "Authorization": f"Basic {client_creds_b64.decode()}" # <base64 encoded client_id:client_secret>
}

r = requests.post(token_url, data=token_data, headers=token_headers)
accessdata = r.json()
access_token = accessdata["access_token"]

valid_request = r.status_code in range(200, 299)
playlist_tracks = []

if valid_request:  
    #url = input("Enter the spotify playlist URL: ")
    #playlist_id = url[url.find('playlist/') + len("playlist/"): url.find('?')]
    headers_get_playlist={
        "Authorization" : f"Bearer {access_token}"
    }
    #url_playlist = "https://api.spotify.com/v1/playlists/" + playlist_id +"/tracks"
    url_playlist = "https://api.spotify.com/v1/playlists/" + "1keGqANUxXBbBny4dtLcf5" +"/tracks"
    r = requests.get(url_playlist ,headers= headers_get_playlist)
    playlist_dict = r.json()

    for items in playlist_dict["items"]:
        temp = str(items["track"]["name"])
        for artists in items["track"]["artists"]:
            temp += " - " + str(artists["name"])
            
        print(temp)
        results = YoutubeSearch(temp, max_results=1).to_dict()
        print(results[0]["url_suffix"])