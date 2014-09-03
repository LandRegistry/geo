import unittest
from geo.resources import postcode_to_osgb34


class PostcodeTestCase(unittest.TestCase):
    def test_valid_postcode_to_eastings_northings(self):
        self.assertEqual(postcode_to_osgb34('sw98jx'), [531095.0, 175399.0])

    def test_valid_non_geopgraphic_postcode_to_eastings_northings(self):
        self.assertFalse(postcode_to_osgb34('bx55at'))

    def test_invalid_postcode_to_eastings_northings(self):
        self.assertFalse(postcode_to_osgb34('XXXX'))

    def test_empty_postcode_to_eastings_northings(self):
        self.assertFalse(postcode_to_osgb34(''))