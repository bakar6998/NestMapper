from django.urls import path
from . import views

urlpatterns = [
    # Get all neighborhoods
    path(
        'neighborhoods/',
        views.get_all_neighborhoods,
        name='all-neighborhoods'
    ),

    # Similar neighborhoods — MUST be before detail URL
    path(
        'neighborhoods/<int:pk>/similar/',
        views.get_similar_neighborhoods,
        name='similar-neighborhoods'
    ),

    # Get single neighborhood detail
    path(
        'neighborhoods/<int:pk>/',
        views.get_neighborhood_detail,
        name='neighborhood-detail'
    ),

    # Get neighborhoods by borough
    path(
        'boroughs/<str:borough>/',
        views.get_neighborhoods_by_borough,
        name='neighborhoods-by-borough'
    ),

    # Compare two neighborhoods
    path(
        'compare/',
        views.compare_neighborhoods,
        name='compare-neighborhoods'
    ),

    # Recommendations
    path(
        'recommend/',
        views.get_recommendations,
        name='recommendations'
    ),

    # Search
    path(
        'search/',
        views.search_neighborhoods,
        name='search-neighborhoods'
    ),
]