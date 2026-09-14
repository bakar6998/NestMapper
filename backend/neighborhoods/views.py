from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    Neighborhood,
    NeighborhoodScore
)
from .serializers import (
    NeighborhoodListSerializer,
    NeighborhoodDetailSerializer
)


@api_view(['GET'])
def get_all_neighborhoods(request):
    """
    GET /api/neighborhoods/

    Returns all neighborhoods with
    basic info and scores.

    Can filter by borough:
    GET /api/neighborhoods/?borough=Brooklyn
    """
    # Get borough filter from URL if provided
    borough = request.query_params.get('borough', None)

    if borough:
        # Filter by borough if provided
        neighborhoods = Neighborhood.objects.filter(
            borough=borough
        )
    else:
        # Return all neighborhoods
        neighborhoods = Neighborhood.objects.all()

    # Serialize the data to JSON
    serializer = NeighborhoodListSerializer(
        neighborhoods,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def get_neighborhood_detail(request, pk):
    """
    GET /api/neighborhoods/1/

    Returns full details of one neighborhood.
    Called when user clicks on a neighborhood
    on the map.
    """
    try:
        neighborhood = Neighborhood.objects.get(pk=pk)
    except Neighborhood.DoesNotExist:
        return Response(
            {'error': 'Neighborhood not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = NeighborhoodDetailSerializer(neighborhood)
    return Response(serializer.data)


@api_view(['GET'])
def get_neighborhoods_by_borough(request, borough):
    """
    GET /api/boroughs/Manhattan/

    Returns all neighborhoods in a
    specific borough.
    """
    neighborhoods = Neighborhood.objects.filter(
        borough=borough
    )

    if not neighborhoods.exists():
        return Response(
            {'error': 'Borough not found'},
            status=status.HTTP_404_NOT_FOUND
        )

    serializer = NeighborhoodListSerializer(
        neighborhoods,
        many=True
    )

    return Response(serializer.data)


@api_view(['GET'])
def compare_neighborhoods(request):
    """
    GET /api/compare/?ids=1,2

    Returns two neighborhoods side by side
    for comparison on the Compare page.
    """
    ids = request.query_params.get('ids', None)

    if not ids:
        return Response(
            {'error': 'Please provide two neighborhood ids'},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Split the ids string into a list
    id_list = ids.split(',')

    if len(id_list) != 2:
        return Response(
            {'error': 'Please provide exactly two ids'},
            status=status.HTTP_400_BAD_REQUEST
        )

    neighborhoods = Neighborhood.objects.filter(
        id__in=id_list
    )

    serializer = NeighborhoodDetailSerializer(
        neighborhoods,
        many=True
    )

    return Response(serializer.data)

@api_view(['POST'])
def get_recommendations(request):
    """
    POST /api/recommend/
    Accepts user preferences
    Returns top 5 matching neighborhoods
    """
    from .recommendation import get_recommendations as recommend
    from .serializers import NeighborhoodDetailSerializer

    try:
        preferences = {
            'budget': request.data.get('budget', 3000),
            'borough': request.data.get('borough', 'Any'),
            'transit_priority': request.data.get('transit_priority', 3),
            'life_situation': request.data.get('life_situation', ''),
            'priorities': request.data.get('priorities', []),
            'needs_accessibility': request.data.get('needs_accessibility', False),
            'has_car': request.data.get('has_car', False),
            'has_children': request.data.get('has_children', False),
            'has_pet': request.data.get('has_pet', False),
        }

        results = recommend(preferences)

        response_data = []
        for item in results:
            serializer = NeighborhoodDetailSerializer(
                item['neighborhood']
            )
            data = serializer.data
            data['match_score'] = item['match_score']
            data['match_percentage'] = item['match_percentage']
            data['reasons'] = item['reasons']
            response_data.append(data)

        return Response(response_data)

    except Exception as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
@api_view(['GET'])
def search_neighborhoods(request):
    """
    GET /api/search/?q=Astorea

    Fuzzy search — finds neighborhoods
    even with spelling mistakes!
    """
    from .search import fuzzy_search

    query = request.query_params.get('q', '')

    if not query:
        return Response(
            {'error': 'Please provide a search query'},
            status=status.HTTP_400_BAD_REQUEST
        )

    results = fuzzy_search(query)

    serializer = NeighborhoodListSerializer(
        results,
        many=True
    )

    return Response(serializer.data)
