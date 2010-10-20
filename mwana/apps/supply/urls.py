
from django.conf.urls.defaults import *
from . import views


urlpatterns = patterns('',
    url(r"^$", views.dashboard, name="supply_dashboard"),
    url(r"^requests/(?P<request_pk>\d+)$", views.request_details, name="supply_request_details"),
    url(r"^locations/(?P<location_pk>\d+)$", views.location_details, name="supply_location_details"),
)
