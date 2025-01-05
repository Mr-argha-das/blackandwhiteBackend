import json
from typing import Optional
from fastapi import APIRouter, HTTPException

from artist.models.artist_models import ArtistTable

router = APIRouter()

@router.get('/api/v1/artists-list')
async def getArtistsList():
    data = ArtistTable.objects.all()
    tojson = data.to_json()
    fromjson = json.loads(tojson)
    return {
        "message": "Here is all artist",
        "data": fromjson,
        "status": 200
    }


@router.get("/api/v1/search-artists")
async def search_artists(name: Optional[str] = None):

    artists = ArtistTable.objects(name__icontains=name)

    if not artists:
        raise HTTPException(status_code=404, detail="No artists found matching the criteria")

    # Convert data to JSON
    tojson = artists.to_json()
    fromjson = json.loads(tojson)

    return {
        "message": "Artists found",
        "data": fromjson,
        "status": 200
    }