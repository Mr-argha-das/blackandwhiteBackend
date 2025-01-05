import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mongoengine import connect, Document, StringField

# Connect to MongoDB
connect('MAINSONGSDATABASE', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/MAINSONGSDATABASE")

# Define the ArtistTable document
class ArtistTable(Document):
    image = StringField(required=True)
    name = StringField(required=True)
    genre_type = StringField(required=True)

# Set up your Spotify API credentials
SPOTIPY_CLIENT_ID = "76a66457171d4c6eb3a75a1247b564f4"
SPOTIPY_CLIENT_SECRET = "7fdebf7b4a5e4fe18dc9c13a32523bc5"

# Authenticate using Client Credentials Flow
client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Function to get all types of Hollywood artists and save to DB
def get_all_hollywood_artists_and_save_to_db(limit=50):
    # Search for Hollywood genre artists across all types of music (no specific genre filter)
    results = sp.search(q="genre:hollywood", type="artist", limit=limit)
    artists = results['artists']['items']
    
    for artist in artists:
        artist_name = artist['name']
        artist_image = artist['images'][0]['url'] if artist['images'] else "No image available"
        artist_genres = ", ".join(artist['genres']) if artist['genres'] else "No genres available"

        # Create and save the artist document in MongoDB
        artist_doc = ArtistTable(
            image=artist_image,
            name=artist_name,
            genre_type=artist_genres
        )
        artist_doc.save()
        print(f"Saved {artist_name} to the database.")

# Example: Fetch and save all Hollywood artists to the database
get_all_hollywood_artists_and_save_to_db()