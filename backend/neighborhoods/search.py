from fuzzywuzzy import fuzz
from .models import Neighborhood
from .serializers import NeighborhoodListSerializer


def fuzzy_search(query, threshold=60):
    """
    Searches neighborhoods by name
    even with spelling mistakes!

    Example:
    "Astorea" → finds "Astoria"
    "Brooklin" → finds "Brooklyn"
    "Wiliamburg" → finds "Williamsburg"

    threshold = minimum similarity score
    60 means 60% similar
    """
    if not query:
        return []

    all_neighborhoods = Neighborhood.objects.all()
    results = []

    for neighborhood in all_neighborhoods:
        # Calculate similarity between
        # search query and neighborhood name
        name_score = fuzz.partial_ratio(
            query.lower(),
            neighborhood.name.lower()
        )

        # Also search by borough name
        borough_score = fuzz.partial_ratio(
            query.lower(),
            neighborhood.borough.lower()
        )

        # Take the highest score
        best_score = max(name_score, borough_score)

        if best_score >= threshold:
            results.append({
                'neighborhood': neighborhood,
                'relevance': best_score
            })

    # Sort by relevance highest first
    results.sort(
        key=lambda x: x['relevance'],
        reverse=True
    )

    # Return top 10 results
    return [item['neighborhood'] for item in results[:10]]