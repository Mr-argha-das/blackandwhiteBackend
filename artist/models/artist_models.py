from mongoengine import Document, StringField, IntField

class ArtistTable(Document):
    image = StringField(required=True)
    name = StringField(required=True)
    genre_type = StringField(required=True)

