from django.urls import path
from . import views

urlpatterns = [
    # Get all neighborhoods
    # GET /api/neighborhoods/
    # GET /api/neighborhoods/?borough=Brooklyn
    path(
        'neighborhoods/',
        views.get_all_neighborhoods,
        name='all-neighborhoods'
    ),

    # Get single neighborhood detail
    # GET /api/neighborhoods/1/
    path(
        'neighborhoods/<int:pk>/',
        views.get_neighborhood_detail,
        name='neighborhood-detail'
    ),

    # Get neighborhoods by borough
    # GET /api/boroughs/Manhattan/
    path(
        'boroughs/<str:borough>/',
        views.get_neighborhoods_by_borough,
        name='neighborhoods-by-borough'
    ),

    # Compare two neighborhoods
    # GET /api/compare/?ids=1,2
    path(
        'compare/',
        views.compare_neighborhoods,
        name='compare-neighborhoods'
    ),

    # Get personalized recommendations
    # POST /api/recommend/
    path(
        'recommend/',
        views.get_recommendations,
        name='recommendations'
    ),
]