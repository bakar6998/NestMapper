from rest_framework import serializers
from .models import (
    Neighborhood,
    RentData,
    TransitInfo,
    SafetyData,
    Amenities,
    AccessibilityData,
    ParkingData,
    NeighborhoodScore
)


class RentDataSerializer(serializers.ModelSerializer):
    """
    Converts RentData model to JSON.
    Shows all rent prices for a neighborhood.
    """
    class Meta:
        model = RentData
        fields = [
            'studio',
            'one_bedroom',
            'two_bedroom',
            'three_bedroom'
        ]


class TransitInfoSerializer(serializers.ModelSerializer):
    """
    Converts TransitInfo model to JSON.
    Shows subway lines, bus routes and
    walkability scores.
    """
    class Meta:
        model = TransitInfo
        fields = [
            'subway_lines',
            'bus_routes',
            'nearest_station',
            'walk_score',
            'transit_score'
        ]


class SafetyDataSerializer(serializers.ModelSerializer):
    """
    Converts SafetyData model to JSON.
    Shows crime statistics.
    """
    class Meta:
        model = SafetyData
        fields = [
            'crime_index',
            'borough_avg_crime',
            'felony_count',
            'misdemeanor_count'
        ]


class AmenitiesSerializer(serializers.ModelSerializer):
    """
    Converts Amenities model to JSON.
    Shows counts of nearby services.
    """
    class Meta:
        model = Amenities
        fields = [
            'schools_count',
            'hospitals_count',
            'parks_count',
            'grocery_stores_count',
            'restaurants_count',
            'pharmacies_count'
        ]


class AccessibilityDataSerializer(serializers.ModelSerializer):
    """
    Converts AccessibilityData model to JSON.
    Shows disability accessibility information.
    This is our unique feature!
    """
    class Meta:
        model = AccessibilityData
        fields = [
            'has_elevator_station',
            'ada_intersections',
            'accessible_parks',
            'accessibility_notes'
        ]


class ParkingDataSerializer(serializers.ModelSerializer):
    """
    Converts ParkingData model to JSON.
    Shows parking difficulty and cost.
    """
    class Meta:
        model = ParkingData
        fields = [
            'difficulty',
            'avg_monthly_garage_cost',
            'street_parking_available',
            'parking_notes'
        ]


class NeighborhoodScoreSerializer(serializers.ModelSerializer):
    """
    Converts NeighborhoodScore model to JSON.
    Shows all computed scores 1-10.
    """
    class Meta:
        model = NeighborhoodScore
        fields = [
            'affordability_score',
            'transit_score',
            'safety_score',
            'family_score',
            'accessibility_score',
            'convenience_score',
            'overall_score'
        ]


class NeighborhoodListSerializer(serializers.ModelSerializer):
    """
    Used for listing all neighborhoods.
    Shows basic info and scores only.
    Keeps the response small and fast.
    """
    scores = NeighborhoodScoreSerializer(read_only=True)
    rent = RentDataSerializer(read_only=True)

    class Meta:
        model = Neighborhood
        fields = [
            'id',
            'name',
            'borough',
            'latitude',
            'longitude',
            'vibe',
            'scores',
            'rent'
        ]


class NeighborhoodDetailSerializer(serializers.ModelSerializer):
    """
    Used for single neighborhood detail.
    Shows ALL information about one neighborhood.
    Called when user clicks on a neighborhood.
    """
    scores = NeighborhoodScoreSerializer(read_only=True)
    rent = RentDataSerializer(read_only=True)
    transit = TransitInfoSerializer(read_only=True)
    safety = SafetyDataSerializer(read_only=True)
    amenities = AmenitiesSerializer(read_only=True)
    accessibility = AccessibilityDataSerializer(read_only=True)
    parking = ParkingDataSerializer(read_only=True)

    class Meta:
        model = Neighborhood
        fields = [
            'id',
            'name',
            'borough',
            'latitude',
            'longitude',
            'description',
            'vibe',
            'scores',
            'rent',
            'transit',
            'safety',
            'amenities',
            'accessibility',
            'parking'
        ]