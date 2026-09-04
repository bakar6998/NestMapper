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

    Accepts user preferences and returns
    top 5 matching neighborhoods.

    Request body:
    {
        "budget": 2000,
        "transit_priority": 4,
        "has_kids": true,
        "has_car": false,
        "needs_accessibility": true,
        "vibe": "Quiet"
    }
    """
    # Get user preferences from request
    budget = request.data.get('budget', 3000)
    transit_priority = request.data.get('transit_priority', 3)
    has_kids = request.data.get('has_kids', False)
    has_car = request.data.get('has_car', False)
    needs_accessibility = request.data.get('needs_accessibility', False)
    vibe = request.data.get('vibe', None)

    # Start with all neighborhoods
    neighborhoods = Neighborhood.objects.all()

    # Filter by vibe if provided
    if vibe:
        neighborhoods = neighborhoods.filter(vibe=vibe)

    # Filter by budget
    # Only show neighborhoods where
    # 1BR rent is within budget + 20%
    # to give some flexibility
    affordable = []
    for n in neighborhoods:
        try:
            if n.rent.one_bedroom <= budget * 1.2:
                affordable.append(n)
        except:
            affordable.append(n)

    # Build dynamic weights based on preferences
    weights = {
        'affordability': 0.20,
        'transit': 0.20,
        'safety': 0.20,
        'family': 0.15,
        'accessibility': 0.10,
        'convenience': 0.15
    }

    # Increase transit weight if high priority
    if transit_priority >= 4:
        weights['transit'] = 0.30
        weights['affordability'] = 0.15

    # Increase family weight if has kids
    if has_kids:
        weights['family'] = 0.25
        weights['safety'] = 0.25
        weights['convenience'] = 0.10

    # Increase accessibility weight if needed
    if needs_accessibility:
        weights['accessibility'] = 0.30
        weights['transit'] = 0.25
        weights['affordability'] = 0.15
        weights['family'] = 0.10
        weights['convenience'] = 0.10
        weights['safety'] = 0.10

    # Calculate match score for each neighborhood
    scored = []
    for n in affordable:
        try:
            scores = n.scores
            match_score = (
                scores.affordability_score * weights['affordability'] +
                scores.transit_score * weights['transit'] +
                scores.safety_score * weights['safety'] +
                scores.family_score * weights['family'] +
                scores.accessibility_score * weights['accessibility'] +
                scores.convenience_score * weights['convenience']
            )
            scored.append({
                'neighborhood': n,
                'match_score': round(match_score, 2)
            })
        except:
            pass

    # Sort by match score highest first
    scored.sort(key=lambda x: x['match_score'], reverse=True)

    # Take top 5 results
    top_5 = scored[:5]

    # Serialize the results
    results = []
    for item in top_5:
        serializer = NeighborhoodDetailSerializer(
            item['neighborhood']
        )
        data = serializer.data
        data['match_score'] = item['match_score']
        results.append(data)

    return Response(results)