from geo import db
from geoalchemy2 import Geometry
from geo import app
import shapely.wkb
from shapely.geometry import mapping
from shapely.geometry import shape
from geoalchemy2.compat import buffer, bytes
import geojson

class Title(db.Model):

    __tablename__ = 'titles'

    id = db.Column(db.Integer, primary_key=True)
    title_number = db.Column(db.String(64))
    extent = db.Column(Geometry('MULTIPOLYGON', srid=app.config['SPATIAL_REFERENCE_SYSTEM_IDENTIFIER']))

    def __init__(self, title_number=None, extent=None):
        self.title_number = title_number
        self.extent = extent

    def __repr__(self):
        return "Title id: %d title number: %s extent: %s" % (self.id, self.title_number, self.extent)

    def set_extent_from_geojson(self, geojson_extent):
        """
        Accepts geojson containing either MultiPolygon or Polygon.
        If it is a Polygon, it is converted to a MultiPolygon
        """
        extent = geojson.loads(geojson_extent)
        if extent['geometry']['type'] == 'Polygon':
            coordinates = []
            coordinates.append(extent['geometry']['coordinates'])
            extent['geometry']['coordinates'] = coordinates
            extent['geometry']['type'] = 'MultiPolygon'

        crs = extent['crs']['properties']['name'].split(':')
        self.extent = 'SRID=%s;%s' % (crs[len(crs) -1] , shape(extent['geometry']).wkt)


    def to_dict(self):
        """
        Returns title number and geojson representing the extent.
        Everything is stored as a multi-polygon, but we convert to a polygon if the 
        multi-polygon contains only 1 polygon
        """

        shape = mapping(shapely.wkb.loads(bytes(self.extent.data)))
        extent = {}
        extent['crs'] = {'type': 'name', 'properties':{'name': 'urn:ogc:def:crs:EPSG:%s' % self.extent.srid}}
        extent['type'] = 'Feature'
        extent['properties'] = {}
        if len(shape['coordinates']) == 1:
            extent['geometry'] = {'coordinates': shape['coordinates'][0], 'type': 'Polygon'}
        else:
            extent['geometry'] = {'coordinates': shape['coordinates'], 'type': 'MultiPolygon'}
        

        return {'title_number': self.title_number, 'extent': extent}