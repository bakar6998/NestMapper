from .models import Neighborhood, NeighborhoodScore


def get_recommendations(preferences):
    """
    Main recommendation function.
    Takes user preferences and returns
    top 5 matching neighborhoods.

    preferences = {
        'budget': 2000,
        'borough': 'Any',
        'transit_priority': 3,
        'life_situation': 'Student',
        'priorities': ['Affordability', 'Safety'],
        'needs_accessibility': False,
        'has_car': False,
        'has_children': False,
        'has_pet': False
    }
    """

    # Step 1 — Get all neighborhoods
    neighborhoods = Neighborhood.objects.all()

    # Step 2 — Filter by borough
    borough = preferences.get('borough', 'Any')
    if borough and borough != 'Any':
        neighborhoods = neighborhoods.filter(
            borough=borough
        )

    # Step 3 — Filter by budget
    budget = preferences.get('budget', 3000)
    affordable = []
    for n in neighborhoods:
        try:
            avg_rent = (
                n.rent.studio +
                n.rent.one_bedroom +
                n.rent.two_bedroom
            ) / 3
            # Allow 20% over budget for flexibility
            if avg_rent <= budget * 1.2:
                affordable.append(n)
        except:
            affordable.append(n)

    if not affordable:
        affordable = list(neighborhoods)

    # Step 4 — Build dynamic weights
    weights = build_weights(preferences)

    # Step 5 — Calculate match score
    scored = []
    for n in affordable:
        try:
            score = n.scores
            match_score = (
                score.affordability_score * weights['affordability'] +
                score.transit_score * weights['transit'] +
                score.safety_score * weights['safety'] +
                score.family_score * weights['family'] +
                score.accessibility_score * weights['accessibility'] +
                score.convenience_score * weights['convenience']
            )

            # Generate reasons why this matches
            reasons = generate_reasons(n, preferences, score)

            scored.append({
                'neighborhood': n,
                'match_score': round(match_score, 2),
                'match_percentage': round(match_score * 10, 1),
                'reasons': reasons
            })
        except Exception as e:
            pass

    # Step 6 — Sort by match score
    scored.sort(
        key=lambda x: x['match_score'],
        reverse=True
    )

    # Step 7 — Return top 5
    return scored[:5]


def build_weights(preferences):
    """
    Builds dynamic weight vector
    based on user preferences.
    All weights must sum to 1.0
    """
    weights = {
        'affordability': 0.20,
        'transit': 0.20,
        'safety': 0.20,
        'family': 0.15,
        'accessibility': 0.10,
        'convenience': 0.15
    }

    transit_priority = preferences.get('transit_priority', 3)
    has_children = preferences.get('has_children', False)
    needs_accessibility = preferences.get('needs_accessibility', False)
    has_car = preferences.get('has_car', False)
    life_situation = preferences.get('life_situation', '')
    priorities = preferences.get('priorities', [])

    # High transit priority
    if transit_priority >= 4:
        weights['transit'] = 0.30
        weights['affordability'] = 0.15

    # Has children
    if has_children:
        weights['family'] = 0.25
        weights['safety'] = 0.25
        weights['convenience'] = 0.10

    # Needs accessibility
    if needs_accessibility:
        weights['accessibility'] = 0.30
        weights['transit'] = 0.25
        weights['affordability'] = 0.15
        weights['family'] = 0.10
        weights['convenience'] = 0.10
        weights['safety'] = 0.10

    # Has car — parking matters more
    if has_car:
        weights['convenience'] = 0.20
        weights['transit'] = 0.10

    # Student — affordability is key
    if life_situation == 'Student':
        weights['affordability'] = 0.35
        weights['transit'] = 0.25
        weights['safety'] = 0.20
        weights['convenience'] = 0.10
        weights['family'] = 0.05
        weights['accessibility'] = 0.05

    # Apply priority boosts
    if 'Affordability' in priorities:
        weights['affordability'] += 0.05
    if 'Safety' in priorities:
        weights['safety'] += 0.05
    if 'Transit' in priorities:
        weights['transit'] += 0.05
    if 'Accessibility' in priorities:
        weights['accessibility'] += 0.05

    # Normalize weights to sum to 1.0
    total = sum(weights.values())
    weights = {k: round(v / total, 3) for k, v in weights.items()}

    return weights


def generate_reasons(neighborhood, preferences, scores):
    """
    Generates human readable reasons
    why this neighborhood matches
    the user's preferences
    """
    reasons = []

    budget = preferences.get('budget', 3000)
    needs_accessibility = preferences.get('needs_accessibility', False)
    has_children = preferences.get('has_children', False)
    transit_priority = preferences.get('transit_priority', 3)

    # Affordability reason
    try:
        avg_rent = (
            neighborhood.rent.studio +
            neighborhood.rent.one_bedroom +
            neighborhood.rent.two_bedroom
        ) / 3

        if avg_rent <= budget:
            reasons.append(
                f"Average rent ${avg_rent:.0f}/mo fits your ${budget} budget"
            )
    except:
        pass

    # Transit reason
    if transit_priority >= 4 and scores.transit_score >= 7:
        try:
            lines = neighborhood.transit.subway_lines
            reasons.append(
                f"Excellent transit with {len(lines)} subway lines"
            )
        except:
            reasons.append("Great public transit access")

    # Safety reason
    if scores.safety_score >= 7:
        reasons.append(
            f"Safe neighborhood scoring {scores.safety_score}/10"
        )

    # Family reason
    if has_children and scores.family_score >= 7:
        try:
            schools = neighborhood.amenities.schools_count
            reasons.append(
                f"{schools} schools nearby — great for families"
            )
        except:
            reasons.append("Family friendly neighborhood")

    # Accessibility reason
    if needs_accessibility:
        try:
            if neighborhood.accessibility.has_elevator_station:
                reasons.append(
                    "Elevator-accessible subway station nearby"
                )
        except:
            pass

    # Vibe reason
    reasons.append(
        f"{neighborhood.vibe} neighborhood atmosphere"
    )

    return reasons[:3]