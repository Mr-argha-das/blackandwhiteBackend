# API to search songs with pagination
from typing import Optional

from fastapi import APIRouter, Query

from config.midlware_routes import MIDLWARE
from songs.models.songs_model import SongTable
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
    
    # Prepare response data
    return {
        "page": page,
        "page_size": page_size,
        "total_songs": total_songs,
        "total_pages": (total_songs + page_size - 1) // page_size,  # total pages calculation
        "songs": [
            {
                "artistsIDs": song.artistsIDs,
                "album_name": song.album_name,
                "image": song.image,
                "title": song.title,
                "genrie_type": song.genrie_type,
                "track_url": song.track_url,
                "like": song.like,
                "played": song.played,
                "lyrics": song.lyrics
            } for song in songs
        ]
    }