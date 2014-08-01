from django.conf.urls import patterns, include, url
import resources

urlpatterns = patterns('',
    url(r'^titles', include(resources.Title.urls())),
)