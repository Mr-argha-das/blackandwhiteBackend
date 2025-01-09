import json
import random
from typing import Optional
from fastapi import APIRouter, HTTPException, Query

from artist.models.artist_models import ArtistTable
from config.midlware_routes import MIDLWARE

router = APIRouter()

@router.get(f'{MIDLWARE}/artists-list')
async def getArtistsList(page: int = Query(1, ge=1), limit: int = Query(10, le=100)):
    """
    Get paginated list of artists, shuffled.
    
    - `page`: the page number to return (default is 1).
    - `limit`: the number of artists per page (default is 10, maximum is 100).
    """
    skip = (page - 1) * limit
    data = ArtistTable.objects.skip(skip).limit(limit)

    # Convert the result to JSON
    tojson = data.to_json()
    fromjson = json.loads(tojson)

    # If no data is found, raise an HTTPException
    if not fromjson:
        raise HTTPException(status_code=404, detail="No artists found.")

    # Shuffle the list of artists
    random.shuffle(fromjson)

    return {
        "message": "Here is the shuffled list of artists",
        "data": fromjson,
        "page": page,
        "limit": limit,
        "status": 200
    }

@router.get(f"{MIDLWARE}/search-artists")
async def search_artists(name: Optional[str] = None):
    if name == None:
        raise HTTPException(status_code=404, detail="Pleasew enter name")
    artists = ArtistTable.objects(name__icontains=name)
    if not artists:
        raise HTTPException(status_code=404, detail="No artists found matching the criteria")
    tojson = artists.to_json()
    fromjson = json.loads(tojson)

    return {
        "message": "Artists found",
        "data": fromjson,
        "status": 200
    }