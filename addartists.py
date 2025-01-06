from bson import ObjectId
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from fastapi import APIRouter, Request

from artist.models.artist_models import ArtistTable
from songs.models.songs_model import SongTable

# Replace these with your credentials
CLIENT_ID = '76a66457171d4c6eb3a75a1247b564f4'
CLIENT_SECRET = '7fdebf7b4a5e4fe18dc9c13a32523bc5'
REDIRECT_URI = 'http://localhost:8000/callback'  # Local redirect URI

# Initialize Spotipy with OAuth
router = APIRouter()

# Initialize Spotipy OAuth manager
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope=["user-library-read"])

# Home page (just to show a link to start authentication)
@router.get("/")
async def home():
    auth_url = sp_oauth.get_authorize_url()
    return {"message": "Go to this URL to authenticate with Spotify", "auth_url": auth_url}

# The callback endpoint that Spotify redirects to
@router.get("/callback")
async def callback(request: Request):
    # Get the authorization code from the URL query parameters
    token_info = sp_oauth.get_access_token(request.query_params["code"])
    
    # Get the access token
    access_token = token_info['access_token']
    
    # Use the access token to create a Spotipy instance
    sp = Spotify(auth=access_token)

    # Example: Search for an artist and get all tracks
    findAllArtist = ArtistTable.objects.all()
    for artistData in findAllArtist:
        artist_name = 'Arijit Singh'  # Change this to the artist you're interested in
        result = sp.search(q='artist:' + artistData.name, type='artist', limit=1)
        
        if not result['artists']['items']:
            return {"error": "Artist not found"}

        artist_id = result['artists']['items'][0]['id']
        artist2 = result['artists']['items'][0]
        artist_genres = artist2['genres']
        # Get all albums by the artist
        albums = sp.artist_albums(artist_id, album_type='album')
        all_tracks = []

        for album in albums['items']:
            album_id = album['id']
            album_name = album['name']
            
            # Get all tracks in the album
            tracks = sp.album_tracks(album_id)

            # Store track info including the album image
            for track in tracks['items']:
                album_details = sp.album(album_id)
                album_image_url = album_details['images'][0]['url'] if album_details['images'] else None
                
                all_tracks.append({
                    "track_name": track['name'],
                    "track_url": track['external_urls']['spotify'],
                    "album_name": album_name,
                    "album_image_url": album_image_url
                })
                savedata = SongTable(
                    artistsIDs = str(ObjectId(artistData.id)),
                    title = track['name'],
                    track_url = track['external_urls']['spotify'],
                    like = ["admin"],
                    played = 0,
                    album_name = album_name,
                    image = album_image_url,
                    genrie_type = artist_genres
                )
                print({
                    "track_name": track['name'],
                    "track_url": track['external_urls']['spotify'],
                    "album_name": album_name,
                    "album_image_url": album_image_url
                })
                savedata.save()
                print("data saved")
            
    
    return {"artist_name": artist_name, "tracks": all_tracks}
