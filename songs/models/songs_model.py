from mongoengine import Document, StringField, IntField, ListField
from pydantic import BaseModel
class SongTable(Document):
    artistsIDs = StringField(required=True)
    album_name = StringField(required=True)
    image = StringField(required=True)
    title = StringField(required=True)
    genrie_type = ListField(required=True)
    track_url = StringField(required=True)
    like = ListField(required=True)
    played=IntField(required=True)
    lyrics = StringField(required=False)

class SongCreateModel(BaseModel):
    artistsIDs : list
    title : str
    genrie_type : str