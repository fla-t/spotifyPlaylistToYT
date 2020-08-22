import requests
import datetime
import base64

client_id = "78104017828e4ae4bcdce82968f74763"
client_secret = "2841edfcac9d4f0288107d08248ffa5c"

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

if valid_request:
    playlist_id = "3FcROySC4sOrVEHOLFGD3i"
    headers_get_playlist={
        "Authorization" : f"Bearer {access_token}"
    }
    url_playlist = "https://api.spotify.com/v1/playlists/" + playlist_id +"/tracks"

r = requests.get(url_playlist ,headers= headers_get_playlist)
print(r.json())
