from mongoengine import Document
from mongoengine.fields import Int64, StringField


class Crosshair(Document):
    author = Int64()  # Steamid64 of author
    config = StringField()  # Short version of the config, space separated numbers
