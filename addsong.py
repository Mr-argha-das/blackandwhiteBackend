import os
import io
from bson import ObjectId
from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch
from boto3 import client
import uuid
from mongoengine import connect

from songs.models.songs_model import SongTable
from track.models.track_model import TrackTable

connect('MAINSONGSDATABASE', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/MAINSONGSDATABASE")

def search_and_download_mp3(song_name):
    # Step 1: Search for the song on YouTube
    videos_search = VideosSearch(song_name, limit=1)
    result = videos_search.result()

    if not result['result']:
        print("No results found.")
        return

    video_url = result['result'][0]['link']
    print(f"Found: {result['result'][0]['title']}\nURL: {video_url}")

    # Step 2: Download the audio as MP3 using yt-dlp
    filename = f"{song_name}.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': filename,  # Save as song_name.mp3
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Downloaded and saved as {filename}")

    # Step 3: Read the MP3 file content into bytes
    with open(f"{filename}.mp3", 'rb') as file:
        file_content = file.read()

    # Step 4: Upload to DigitalOcean Spaces
    uploaded_url = upload_file_to_space(file_content, filename)
    print(f"File uploaded to: {uploaded_url}")

    # Step 5: Delete the MP3 file
    os.remove(f"{filename}.mp3")
    print(f"Deleted local file: {filename}")

    return uploaded_url


def upload_file_to_space(file_content: bytes, filename: str):
    spaces_access_key = 'DO00AJFUXFALT4K6L69E'
    spaces_secret_key = 'kn2jUm8ox9W6fPQXvJ6E5kBtVZtzF5V5MvY6sJ8Cr8U'
    spaces_endpoint_url = 'https://blackwhite.blr1.digitaloceanspaces.com'
    spaces_bucket_name = 'BlackandWhite'

    # Generate a random filename using UUID
    random_filename = str(uuid.uuid4())
    file_extension = os.path.splitext(filename)[1]  # Extract file extension from the original filename
    random_filename_with_extension = f"{random_filename}{file_extension}"

    s3 = client('s3',
                region_name='blr1',
                endpoint_url=spaces_endpoint_url,
                aws_access_key_id=spaces_access_key,
                aws_secret_access_key=spaces_secret_key)

    # Create a BytesIO object to read file content from memory
    file_content_stream = io.BytesIO(file_content)

    s3.upload_fileobj(
        file_content_stream,
        spaces_bucket_name,
        random_filename_with_extension,
        ExtraArgs={'ACL': 'public-read'}
    )

    return f"{spaces_endpoint_url}/BlackandWhite/{random_filename_with_extension}"


# Example usage
# song_name = "Channa Mereya (From Ae Dil Hai Mushkil)"
# uploaded_url = search_and_download_mp3(song_name)
# print(f"Uploaded MP3 URL: {uploaded_url}")

findata = SongTable.objects.all()
for index, song in enumerate(findata):
    if index > 1094:
        try:
           uploadedurl = search_and_download_mp3(str(song.title))
           savedata = TrackTable(songId=str(ObjectId(song.id)), url=uploadedurl)
           savedata.save()
           print(f"Saved: {song.title} (Index ID: {index})")
        except Exception as e:
           print(f"Error arghadas (Index ID: {index}): {e}")
           continue