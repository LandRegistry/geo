from geo import db
from geoalchemy2 import Geometry
from geo import app

class Title(db.Model):

    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64))
    extent = db.Column(Geometry('MULTIPOLYGON', srid=app.config['SPATIAL_REFERENCE_SYSTEM_IDENTIFIER']))

    def __init__(self, title_number, extent):
        self.title_number = title_number
        self.extent = extent

    def __repr__(self):
        return "Title id: %d title number: %s extent: %s" % (self.id, self.title_number, self.extent)
