import numpy as np
from .models import Neighborhood
from .serializers import NeighborhoodListSerializer


def get_similar_neighborhoods(neighborhood_id, limit=3):
    """
    Finds neighborhoods most similar
    to a given neighborhood.

    Uses Euclidean Distance algorithm
    Same concept as KNN (K Nearest Neighbors)

    Example:
    User clicks Astoria
    App finds 3 most similar neighborhoods
    "You might also like Jackson Heights"

    Lower distance = more similar
    """
    try:
        # Get target neighborhood
        target = Neighborhood.objects.get(pk=neighborhood_id)
        target_scores = target.scores
    except Neighborhood.DoesNotExist:
        return []
    except Exception:
        return []

    # Build target score vector
    target_vector = np.array([
        target_scores.affordability_score,
        target_scores.transit_score,
        target_scores.safety_score,
        target_scores.family_score,
        target_scores.accessibility_score,
        target_scores.convenience_score,
    ])

    # Get all other neighborhoods
    all_neighborhoods = Neighborhood.objects.exclude(
        pk=neighborhood_id
    )

    similarities = []

    for n in all_neighborhoods:
        try:
            n_scores = n.scores

            # Build comparison vector
            n_vector = np.array([
                n_scores.affordability_score,
                n_scores.transit_score,
                n_scores.safety_score,
                n_scores.family_score,
                n_scores.accessibility_score,
                n_scores.convenience_score,
            ])

            # Calculate Euclidean distance
            # Lower = more similar
            distance = np.linalg.norm(
                target_vector - n_vector
            )

            # Convert to similarity score 0-100
            # Max possible distance is ~28
            # (sqrt of 6 * 10^2)
            similarity = round(
                max(0, (1 - distance / 28) * 100), 1
            )

            similarities.append({
                'neighborhood': n,
                'similarity': similarity,
                'distance': round(float(distance), 2)
            })

        except Exception:
            pass

    # Sort by most similar first
    similarities.sort(
        key=lambda x: x['similarity'],
        reverse=True
    )

    # Return top results
    return similarities[:limit]