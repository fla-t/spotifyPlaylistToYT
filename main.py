import os
import requests
import datetime
import base64
import json
import unicodedata
from dotenv import load_dotenv
from youtube_search import YoutubeSearch

client_id = "78104017828e4ae4bcdce82968f74763"
client_secret = "59d0bfe6d81146518eeccc078e2cdb0a"

client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

token_url = "https://accounts.spotify.com/api/token"
method = "POST"
token_data = {
    "grant_type": "client_credentials"
}
token_headers = {
    "Authorization": f"Basic {client_creds_b64.decode()}"
}

r = requests.post(token_url, data=token_data, headers=token_headers)
accessdata = r.json()
access_token = accessdata["access_token"]

valid_request = r.status_code in range(200, 299)
playlist_tracks = []

filehandle = open("links.txt","a")

if valid_request:  
    url = input("Enter the spotify playlist URL: ")
    playlist_id = url[url.find('playlist/') + len("playlist/"): url.find('?')]
    headers_get_playlist={
        "Authorization" : f"Bearer {access_token}"
    }
    url_playlist = "https://api.spotify.com/v1/playlists/" + playlist_id +"/tracks"
    r = requests.get(url_playlist ,headers= headers_get_playlist)
    playlist_dict = r.json()

    for items in playlist_dict["items"]:
        temp = str(items["track"]["name"])
        for artists in items["track"]["artists"]:
            temp += " - " + str(artists["name"])

        try:
            temp = unicode(temp, 'utf-8')
        except NameError: # unicode is a default on python 3 
            pass

        temp = unicodedata.normalize('NFD', temp).encode('ascii', 'ignore').decode("utf-8")
        
        print(temp)
        results = YoutubeSearch(temp, max_results=1).to_dict()
        filehandle.write("youtube.com" + results[0]["url_suffix"] + "\n")
        

filehandle.close()