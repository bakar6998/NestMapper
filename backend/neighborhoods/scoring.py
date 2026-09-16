import numpy as np
from .models import (
    Neighborhood,
    RentData,
    SafetyData,
    TransitInfo,
    Amenities,
    AccessibilityData,
    ParkingData,
    NeighborhoodScore
)


def min_max_normalize(value, min_val, max_val, inverse=False):
    """
    Converts raw value to 1-10 scale
    inverse=True means lower value = higher score
    Used for rent and crime (lower is better)
    """
    if max_val == min_val:
        return 5.0

    score = 1 + 9 * ((value - min_val) / (max_val - min_val))

    if inverse:
        score = 11 - score

    return round(min(max(score, 1.0), 10.0), 2)


def calculate_affordability_score(rent, min_rent, max_rent):
    """
    Lower rent = higher affordability score
    Uses inverse normalization
    """
    avg_rent = (rent.studio + rent.one_bedroom + rent.two_bedroom) / 3
    return min_max_normalize(avg_rent, min_rent, max_rent, inverse=True)


def calculate_transit_score(transit):
    """
    Weighted combination of:
    → Subway lines count 50%
    → Walk score 30%
    → Bus routes count 20%
    """
    subway_count = len(transit.subway_lines)
    bus_count = len(transit.bus_routes)
    walk = transit.walk_score

    # Normalize each component
    subway_score = min(subway_count / 8 * 10, 10)
    bus_score = min(bus_count / 10 * 10, 10)
    walk_score = walk / 10

    # Weighted combination
    score = (
        subway_score * 0.50 +
        walk_score * 0.30 +
        bus_score * 0.20
    )

    return round(min(max(score, 1.0), 10.0), 2)


def calculate_safety_score(safety, min_crime, max_crime):
    """
    Lower crime = higher safety score
    Uses inverse normalization
    """
    return min_max_normalize(
        safety.crime_index,
        min_crime,
        max_crime,
        inverse=True
    )


def calculate_family_score(amenities):
    """
    Weighted combination of:
    → Schools 40%
    → Parks 30%
    → Hospitals 30%
    """
    school_score = min(amenities.schools_count / 15 * 10, 10)
    park_score = min(amenities.parks_count / 10 * 10, 10)
    hospital_score = min(amenities.hospitals_count / 5 * 10, 10)

    score = (
        school_score * 0.40 +
        park_score * 0.30 +
        hospital_score * 0.30
    )

    return round(min(max(score, 1.0), 10.0), 2)


def calculate_accessibility_score(accessibility):
    """
    Weighted combination of:
    → Elevator station 40%
    → ADA intersections 35%
    → Accessible parks 25%
    """
    elevator_score = 10.0 if accessibility.has_elevator_station else 2.0
    ada_score = min(accessibility.ada_intersections / 50 * 10, 10)
    parks_score = min(accessibility.accessible_parks / 5 * 10, 10)

    score = (
        elevator_score * 0.40 +
        ada_score * 0.35 +
        parks_score * 0.25
    )

    return round(min(max(score, 1.0), 10.0), 2)


def calculate_convenience_score(amenities):
    """
    Weighted combination of:
    → Grocery stores 40%
    → Restaurants 30%
    → Pharmacies 30%
    """
    grocery_score = min(amenities.grocery_stores_count / 10 * 10, 10)
    restaurant_score = min(amenities.restaurants_count / 20 * 10, 10)
    pharmacy_score = min(amenities.pharmacies_count / 5 * 10, 10)

    score = (
        grocery_score * 0.40 +
        restaurant_score * 0.30 +
        pharmacy_score * 0.30
    )

    return round(min(max(score, 1.0), 10.0), 2)


def calculate_overall_score(scores):
    """
    Equal weighted average of all
    6 dimension scores
    """
    total = (
        scores['affordability'] +
        scores['transit'] +
        scores['safety'] +
        scores['family'] +
        scores['accessibility'] +
        scores['convenience']
    ) / 6

    return round(total, 2)


def compute_all_scores():
    """
    Main function that computes scores
    for ALL neighborhoods in database
    Called by compute_scores.py command
    """
    neighborhoods = Neighborhood.objects.all()

    if not neighborhoods.exists():
        print("No neighborhoods found in database")
        return

    # Get min and max values for normalization
    rent_avgs = []
    crime_indices = []

    for n in neighborhoods:
        try:
            avg = (
                n.rent.studio +
                n.rent.one_bedroom +
                n.rent.two_bedroom
            ) / 3
            rent_avgs.append(avg)
        except:
            pass

        try:
            crime_indices.append(n.safety.crime_index)
        except:
            pass

    # Calculate min and max
    min_rent = min(rent_avgs) if rent_avgs else 1000
    max_rent = max(rent_avgs) if rent_avgs else 5000
    min_crime = min(crime_indices) if crime_indices else 0
    max_crime = max(crime_indices) if crime_indices else 1000

    print(f"Computing scores for {neighborhoods.count()} neighborhoods...")
    print(f"Rent range: ${min_rent:.0f} - ${max_rent:.0f}")
    print(f"Crime range: {min_crime:.0f} - {max_crime:.0f}")

    success = 0
    errors = 0

    for n in neighborhoods:
        try:
            scores = {}

            # Affordability
            try:
                scores['affordability'] = calculate_affordability_score(
                    n.rent, min_rent, max_rent
                )
            except:
                scores['affordability'] = 5.0

            # Transit
            try:
                scores['transit'] = calculate_transit_score(n.transit)
            except:
                scores['transit'] = 5.0

            # Safety
            try:
                scores['safety'] = calculate_safety_score(
                    n.safety, min_crime, max_crime
                )
            except:
                scores['safety'] = 5.0

            # Family
            try:
                scores['family'] = calculate_family_score(n.amenities)
            except:
                scores['family'] = 5.0

            # Accessibility
            try:
                scores['accessibility'] = calculate_accessibility_score(
                    n.accessibility
                )
            except:
                scores['accessibility'] = 5.0

            # Convenience
            try:
                scores['convenience'] = calculate_convenience_score(
                    n.amenities
                )
            except:
                scores['convenience'] = 5.0

            # Overall
            scores['overall'] = calculate_overall_score(scores)

            # Save or update scores
            NeighborhoodScore.objects.update_or_create(
                neighborhood=n,
                defaults={
                    'affordability_score': scores['affordability'],
                    'transit_score': scores['transit'],
                    'safety_score': scores['safety'],
                    'family_score': scores['family'],
                    'accessibility_score': scores['accessibility'],
                    'convenience_score': scores['convenience'],
                    'overall_score': scores['overall'],
                }
            )

            print(f"✅ {n.name} — Overall: {scores['overall']}")
            success += 1

        except Exception as e:
            print(f"❌ Error for {n.name}: {e}")
            errors += 1

    print(f"\nDone! {success} scored, {errors} errors")