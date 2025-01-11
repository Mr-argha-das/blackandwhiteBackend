# API to search songs with pagination
import json
import math
import random
from typing import List, Optional

from bson import ObjectId
from fastapi import APIRouter, HTTPException, Query

from artist.models.artist_models import ArtistTable
from config.midlware_routes import MIDLWARE
from songs.models.songs_model import SongRecommendation, SongTable
from track.models.track_model import TrackTable
from userhestory.models.usershistory import UserHistoryTable
router = APIRouter()

@router.get(f"{MIDLWARE}/songs/")
def search_songs(
    title: Optional[str] = Query(None, description="Search by song title"),
    album_name: Optional[str] = Query(None, description="Search by album name"),
    page: int = Query(1, description="Page number"),
    page_size: int = Query(10, description="Number of items per page")
):
    query = {}
    
    # Building the query based on title or album_name
    if title:
        query["title__icontains"] = title
    if album_name:
        query["album_name__icontains"] = album_name
    
    # Pagination calculations
    skip = (page - 1) * page_size
    
    # Query the database
    songs = SongTable.objects(**query).skip(skip).limit(page_size)
    total_songs = SongTable.objects(**query).count()
    
    # Shuffle the songs randomly
    song_list = [
        {   
            "_id": str(song.id),
            "artistsIDs": song.artistsIDs,
            "artists": json.loads(ArtistTable.objects.get(id=ObjectId(song.artistsIDs)).to_json()),
            "album_name": song.album_name,
            "image": song.image,
            "title": song.title,
            "genrie_type": song.genrie_type,
            "track_url": song.track_url,
            "like": song.like,
            "played": song.played,
            "lyrics": song.lyrics,
            "track": json.loads(TrackTable.objects(songId=str(ObjectId(song.id))).to_json())[0]
        } for song in songs
    ]
    
    # Randomly shuffle the song list
    random.shuffle(song_list)
    
    # Prepare response data
    return {
        "page": page,
        "page_size": page_size,
        "total_songs": total_songs,
        "total_pages": (total_songs + page_size - 1) // page_size,  # total pages calculation
        "songs": song_list,
        "status": 200
    }

@router.get(f"{MIDLWARE}/update-played/song/{id}")
async def updatePlayedSong(id:str):
    findata = SongTable.objects.get(id=ObjectId(str(id)))
    findata.played = findata.played + 1
    findata.save()
    return {
        "message": "Song played updated",
        "status": 200
    }

@router.get(f"{MIDLWARE}/update-played/song/")
async def updateLikeSong(songid:str,userid:str ):
    findata = SongTable.objects.get(id=ObjectId(str(songid)))
    findata.like.append(userid)
    findata.save()
    return {
        "message": "Thank you for giveing me a like",
        "status": 200
    }

@router.get(f"{MIDLWARE}/add-song/user-history")
async def addSongUserHistory(userid: str, songid:str):
    sondata = SongTable.objects.get(id=ObjectId(songid))
    savedata = UserHistoryTable(userid=userid,songData=sondata)
    savedata.save()
    return {
        "message": "History update",
        "status": 200
    }
def song_to_pydantic(song):
    return SongRecommendation(
        artistsIDs=song.artistsIDs,
        album_name=song.album_name,
        image=song.image,
        title=song.title,
        genrie_type=song.genrie_type,
        track_url=song.track_url,
        like=song.like,
        played=song.played,

    )
@router.get("/api/v1/recommend_songs/{userid}", response_model=List[SongRecommendation])
def recommend_songs(userid: str, limit: int = 5):
    """
    Recommend songs based on the user's recent play history.
    Fetches recent songs the user has listened to and recommends similar songs.
    """
    try:
        # Get the user's song history from UserHistoryTable
        user_history = UserHistoryTable.objects(userid=userid).order_by('-id').limit(limit)
        
        if not user_history:
            raise HTTPException(status_code=404, detail="No history found for this user")

        # Collect all songs the user has played recently
        recent_songs = [entry.songData for entry in user_history]

        # Get the IDs of recent songs to exclude from recommendations
        recent_song_ids = [song.id for song in recent_songs]

        # Fetch more songs based on the genre or artist of the recent songs
        recommendations = SongTable.objects(
            artistsIDs__in=[song.artistsIDs for song in recent_songs],  # Match by artist
            genrie_type__in=[genre for song in recent_songs for genre in song.genrie_type]  # Match by genre
        ).filter(id__nin=recent_song_ids)  # Exclude already played songs

        # Limit the number of recommendations
        recommendations = recommendations[:limit]

        # Convert to Pydantic models for response
        response = [{
            "artistsIDs":song.artistsIDs,
        "album_name":song.album_name,
        "image":song.image,
        "title":song.title,
        "genrie_type":song.genrie_type,
        "track_url":song.track_url,
        "like":song.like,
        "played":song.played,
        "artist" : json.loads(ArtistTable.objects.get(id=ObjectId(song.artistsIDs)).to_json()),
        "track": json.loads(TrackTable.objects(songId=str(ObjectId(song.id))).to_json())
            } for song in recommendations]
        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/shuffle_songs/")
async def shuffle_songs():
    # Fetch all songs from the database
    songs = SongTable.objects.all()
    
    # Shuffle the songs list in place
    shuffled_songs = list(songs)
    random.shuffle(shuffled_songs)
    
    # Save the shuffled order back to the database
    for idx, song in enumerate(shuffled_songs):
        # Optionally, if you have a 'position' or 'order' field, you can update that field
        # song.update(set__position=idx)
        
        # If you don't need to update specific fields, simply save it back
        song.save()
    
    return {"message": "Songs shuffled and saved successfully.", "status": 200}

@router.get(f"{MIDLWARE}/random-songs")
async def randomSongs(page: int = 1, limit: int = 10):
    songsList = []
    
    # Fetch all songs
    songs = SongTable.objects.all()
    
    # Ensure the page and limit are valid
    if page < 1:
        raise HTTPException(status_code=400, detail="Page must be greater than or equal to 1")
    if limit < 1:
        raise HTTPException(status_code=400, detail="Limit must be greater than or equal to 1")
    
    # Calculate the starting index and ending index for pagination
    start_index = (page - 1) * limit
    end_index = start_index + limit

    # If there are more songs than the current page + limit, shuffle the list
    shuffled_songs = list(songs)  # Convert to list so we can shuffle
    random.shuffle(shuffled_songs)
    
    # Slice the list based on the page and limit
    paginated_songs = shuffled_songs[start_index:end_index]
    
    # Fetch data for each song
    for song in paginated_songs:
        artists = json.loads(ArtistTable.objects.get(id=ObjectId(song.artistsIDs)).to_json())
        track = json.loads(TrackTable.objects(songId=str(ObjectId(song.id))).to_json())
        songsList.append({
            "song": json.loads(song.to_json()),
            "artist": artists,
            "track": track
        })
    
    # Calculate the total number of pages
    total_songs = len(songs)
    total_pages = math.ceil(total_songs / limit)
    
    # Return response with pagination metadata
    return {
        "message": "Here is data",
        "data": songsList,
        "pagination": {
            "page": page,
            "limit": limit,
            "total_songs": total_songs,
            "total_pages": total_pages
        },
        "status": 200
    }