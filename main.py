from fastapi import FastAPI
from mongoengine import connect
from artist.routes import artists_routes
connect('MAINSONGSDATABASE', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/MAINSONGSDATABASE")
app = FastAPI()

app.include_router(artists_routes.router, tags=["Clients"])