from django.contrib.gis.db import models
import settings

class Title(models.Model):

	#fields
	title_number = models.CharField(max_length=100, unique=True)
	area = models.PolygonField(srid=settings.SRID)

	#manager
	objects = models.GeoManager()