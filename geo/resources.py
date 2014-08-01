from restless.dj import DjangoResource
import models

class Title(DjangoResource):

    def list(self):
    	return models.Title.objects.all()
