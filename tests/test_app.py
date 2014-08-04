from geo import server, db
import json
import unittest


class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_get_unknown_title(self):
        response = self.app.get('/titles/TN99999')
        assert response.status_code == 404

    def test_put_title(self):
    	extent = '{   "type": "Feature",   "crs": {     "type": "name",     "properties": {       "name": "urn:ogc:def:crs:EPSG:27700"     }   },   "geometry": {      "type": "Polygon",     "coordinates": [       [ [530857.01, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.01, 181500.00] ]       ]   },   "properties" : {      } }'
        response = self.app.put('/titles/DN100' ,
                                data='{"title_number":"DN100", "extent": extent}',
                                content_type='application/json')

        assert response.status_code == 201    