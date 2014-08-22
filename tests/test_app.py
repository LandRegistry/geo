from geo import server, db
import json
import unittest
from geo.resources import postcode_to_osgb34

class AppTestCase(unittest.TestCase):

    def setUp(self):
        db.create_all()
        self.app = server.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_postcode_to_eastings_northings(self):
        
        #valid geographic postcode
        location = postcode_to_osgb34('sw98jx')
        assert location == [531093, 175405]

        #valid, non-geographic postcode
        self.assertFalse(postcode_to_osgb34('bx55at'))
        
        #invalid
        self.assertFalse(postcode_to_osgb34('XXXX'))
        self.assertFalse(postcode_to_osgb34(''))


    def test_postcode(self):

        #missing postcode
        response = self.app.get('/titles?method=near-postcode&location=')
        assert response.status_code == 400
        assert 'Postcode not supplied' in response.data

        #invalid postcode
        response = self.app.get('/titles?method=near-postcode&location=XXXXX')
        assert response.status_code == 400
        assert 'Invalid postcode' in response.data

        #non-geographical postcode
        response = self.app.get('/titles?method=near-postcode&location=bx55at')
        assert response.status_code == 500
        assert 'Unable to convert valid postcode to OSGB34' in response.data

        #valid
        response = self.app.get('/titles?method=near-postcode&location=sw98jx')

    def test_get_unknown_title(self):
        """
        Check for a valid 404
        """
        response = self.app.get('/titles/TN99999')
        assert response.status_code == 404

    # def load_sample_data(self, count):

    #     counter = 0

    #     extent = '{   "type": "Feature",   "crs": {     "type": "name",     "properties": {       "name": "urn:ogc:def:crs:EPSG:27700"     }   },   "geometry": {      "type": "Point",     "coordinates": [530857.01, 181500.00]  },   "properties" : {      } }'
    #     response = self.app.put('/titles/DN104' ,
    #                         data='{"title_number":"DN104", "extent": %s}' % json.dumps(extent),
    #                         content_type='application/json')

    #     assert response.status_code == 200
    #     counter = counter + 1

    # def test_get_list(self):

    #     response = self.app.get('/titles')
    #     assert response.status_code == 200
    #     assert len(json.loads(response.data)) == 0

    #     #add some examples
    #     self.load_sample_data(10)

    #     #check exists
    #     response = self.app.get('/titles')
    #     assert len(json.loads(response.data)) == 10
    #     assert 'DN104' in response

    #     #check near search
    #     response = self.app.get('/titles?method=near&location={"type": "Point","coordinates": [30, 10]}')


    def test_put_point(self):
        """
        Make sure we cannot save a point
        """
        extent = '{   "type": "Feature",   "crs": {     "type": "name",     "properties": {       "name": "urn:ogc:def:crs:EPSG:27700"     }   },   "geometry": {      "type": "Point",     "coordinates": [530857.01, 181500.00]  },   "properties" : {      } }'
        response = self.app.put('/titles/DN104' ,
                                data='{"title_number":"DN104", "extent": %s}' % json.dumps(extent),
                                content_type='application/json')

        assert response.status_code == 400

    def test_put_get_polygon(self):
        """
        Save and view a polygon
        """
        extent = '{   "type": "Feature",   "crs": {     "type": "name",     "properties": {       "name": "urn:ogc:def:crs:EPSG:27700"     }   },   "geometry": {      "type": "Polygon",     "coordinates": [       [ [530857.01, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.01, 181500.00] ]       ]   },   "properties" : {      } }'
        response = self.app.put('/titles/DN100' ,
                                data='{"title_number":"DN100", "extent": %s}' % json.dumps(extent),
                                content_type='application/json')

        assert response.status_code == 200

        response = self.app.get('/titles/DN100')
        assert response.status_code == 200


    def test_put_get_multipolygon(self):
        """
        Save and view a multipolygon
        """

        extent = '{   "type": "Feature",   "crs": {     "type": "name",     "properties": {       "name": "urn:ogc:def:crs:EPSG:27700"     }   },   "geometry": {      "type": "MultiPolygon",     "coordinates": [[       [ [530857.01, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.00, 181500.00], [530857.01, 181500.00] ]       ] ]  },   "properties" : {      } }'
        response = self.app.put('/titles/DN101' ,
                                data='{"title_number":"DN100", "extent": %s}' % json.dumps(extent),
                                content_type='application/json')

        assert response.status_code == 200

        response = self.app.get('/titles/DN101')
        assert response.status_code == 200