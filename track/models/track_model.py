from mongoengine import Document, StringField,connect
#connect('MAINSONGSDATABASE', host="mongodb+srv://avbigbuddy:nZ4ATPTwJjzYnm20@cluster0.wplpkxz.mongodb.net/MAINSONGSDATABASE")
class TrackTable(Document):
    songId = StringField(required=True)
    url = StringField(required=True)