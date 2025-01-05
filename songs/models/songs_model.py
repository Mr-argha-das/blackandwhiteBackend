from mongoengine import Document, StringField, IntField, ListField
from pydantic import BaseModel
class SongTable(Document):
    artistsIDs = ListField(required=True)
    title = StringField(required=True)
    genrie_type = ListField(required=True)
    like = ListField(required=True)
    played=ListField(required=True)
    lyrics = StringField(required=False)

class SongCreateModel(BaseModel):
    artistsIDs : list
    title : str
    genrie_type : str