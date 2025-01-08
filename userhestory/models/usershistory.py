from mongoengine import Document, StringField, ReferenceField

from songs.models.songs_model import SongTable

class UserHistoryTable(Document):
    userid = StringField(required=True)
    songData = ReferenceField(SongTable, requirdd=True)