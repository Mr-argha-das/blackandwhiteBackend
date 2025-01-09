from fastapi import FastAPI
from mongoengine import connect
import addartists
from artist.routes import artists_routes
from songs.routes import songsrouts
connect('MAINSONGSDATABASE', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/MAINSONGSDATABASE")
app = FastAPI()
app.include_router(addartists.router, tags=["add Artists"])
app.include_router(artists_routes.router, tags=["Artist"])
app.include_router(songsrouts.router, tags=["songs routes"])
import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", port=8080, reload=True)