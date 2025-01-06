from yt_dlp import YoutubeDL
from youtubesearchpython import VideosSearch

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
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'{song_name}.mp3',  # Name the file as the song_name
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    print(f"Downloaded and saved as {song_name}.mp3")

# Example usage
song_name = "Aditya Rikhari - Humdum"
search_and_download_mp3(song_name)
