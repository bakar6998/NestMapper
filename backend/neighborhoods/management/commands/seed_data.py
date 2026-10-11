"""
seed_data.py
Loads real NYC neighborhood data
into PostgreSQL database

Run with:
python manage.py seed_data
"""

from django.core.management.base import BaseCommand
from neighborhoods.models import (
    Neighborhood,
    RentData,
    TransitInfo,
    SafetyData,
    Amenities,
    AccessibilityData,
    ParkingData,
    NeighborhoodScore
)

# Original 20 neighborhoods
NEIGHBORHOODS_DATA = [
    # MANHATTAN
    {
        'name': 'Upper West Side',
        'borough': 'Manhattan',
        'latitude': 40.7870,
        'longitude': -73.9754,
        'description': 'Classic Manhattan neighborhood with cultural institutions and Central Park access',
        'vibe': 'Mixed',
        'rent': {'studio': 2800, 'one_bedroom': 3800, 'two_bedroom': 5200, 'three_bedroom': 7500},
        'transit': {'subway_lines': ['1', '2', '3', 'B', 'C'], 'bus_routes': ['M10', 'M11', 'M72'], 'nearest_station': '72nd Street', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 310, 'borough_avg_crime': 420, 'felony_count': 650, 'misdemeanor_count': 980},
        'amenities': {'schools_count': 22, 'hospitals_count': 5, 'parks_count': 8, 'grocery_stores_count': 20, 'restaurants_count': 80, 'pharmacies_count': 12},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 65, 'accessible_parks': 6, 'accessibility_notes': 'Excellent accessibility'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 600, 'street_parking_available': False}
    },
    {
        'name': 'Harlem',
        'borough': 'Manhattan',
        'latitude': 40.8116,
        'longitude': -73.9465,
        'description': 'Historic neighborhood with rich cultural heritage and improving amenities',
        'vibe': 'Lively',
        'rent': {'studio': 1800, 'one_bedroom': 2400, 'two_bedroom': 3200, 'three_bedroom': 4500},
        'transit': {'subway_lines': ['2', '3', 'A', 'B', 'C', 'D'], 'bus_routes': ['M1', 'M2', 'M102'], 'nearest_station': '125th Street', 'walk_score': 96, 'transit_score': 95},
        'safety': {'crime_index': 480, 'borough_avg_crime': 420, 'felony_count': 980, 'misdemeanor_count': 1400},
        'amenities': {'schools_count': 20, 'hospitals_count': 4, 'parks_count': 10, 'grocery_stores_count': 16, 'restaurants_count': 50, 'pharmacies_count': 9},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 52, 'accessible_parks': 5, 'accessibility_notes': 'Good transit accessibility'},
        'parking': {'difficulty': 'Hard', 'avg_monthly_garage_cost': 350, 'street_parking_available': True}
    },
    {
        'name': 'East Village',
        'borough': 'Manhattan',
        'latitude': 40.7265,
        'longitude': -73.9815,
        'description': 'Vibrant neighborhood known for nightlife, dining and arts scene',
        'vibe': 'Lively',
        'rent': {'studio': 2500, 'one_bedroom': 3400, 'two_bedroom': 4800, 'three_bedroom': 6500},
        'transit': {'subway_lines': ['4', '5', '6', 'L', 'N', 'Q', 'R'], 'bus_routes': ['M8', 'M14'], 'nearest_station': '14th Street', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 380, 'borough_avg_crime': 420, 'felony_count': 720, 'misdemeanor_count': 1100},
        'amenities': {'schools_count': 15, 'hospitals_count': 3, 'parks_count': 6, 'grocery_stores_count': 18, 'restaurants_count': 90, 'pharmacies_count': 10},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 58, 'accessible_parks': 4, 'accessibility_notes': 'Good ADA infrastructure'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 550, 'street_parking_available': False}
    },
    {
        'name': 'Washington Heights',
        'borough': 'Manhattan',
        'latitude': 40.8448,
        'longitude': -73.9393,
        'description': 'Diverse neighborhood with Dominican culture and affordable rents for Manhattan',
        'vibe': 'Lively',
        'rent': {'studio': 1600, 'one_bedroom': 2100, 'two_bedroom': 2800, 'three_bedroom': 3800},
        'transit': {'subway_lines': ['1', 'A', 'C'], 'bus_routes': ['M3', 'M4', 'M98'], 'nearest_station': '181st Street', 'walk_score': 95, 'transit_score': 88},
        'safety': {'crime_index': 420, 'borough_avg_crime': 420, 'felony_count': 850, 'misdemeanor_count': 1200},
        'amenities': {'schools_count': 18, 'hospitals_count': 3, 'parks_count': 8, 'grocery_stores_count': 14, 'restaurants_count': 45, 'pharmacies_count': 8},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 48, 'accessible_parks': 4, 'accessibility_notes': 'Good subway accessibility'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 280, 'street_parking_available': True}
    },
    {
        'name': 'Chelsea',
        'borough': 'Manhattan',
        'latitude': 40.7465,
        'longitude': -74.0014,
        'description': 'Trendy neighborhood with art galleries, the High Line and vibrant nightlife',
        'vibe': 'Lively',
        'rent': {'studio': 3000, 'one_bedroom': 4200, 'two_bedroom': 6000, 'three_bedroom': 8500},
        'transit': {'subway_lines': ['1', 'C', 'E'], 'bus_routes': ['M11', 'M14', 'M23'], 'nearest_station': '23rd Street', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 320, 'borough_avg_crime': 420, 'felony_count': 580, 'misdemeanor_count': 920},
        'amenities': {'schools_count': 12, 'hospitals_count': 2, 'parks_count': 5, 'grocery_stores_count': 15, 'restaurants_count': 85, 'pharmacies_count': 8},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 62, 'accessible_parks': 3, 'accessibility_notes': 'High Line is fully accessible'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 650, 'street_parking_available': False}
    },
    # BROOKLYN
    {
        'name': 'Park Slope',
        'borough': 'Brooklyn',
        'latitude': 40.6728,
        'longitude': -73.9797,
        'description': 'Family friendly neighborhood with beautiful brownstones and Prospect Park',
        'vibe': 'Mixed',
        'rent': {'studio': 2400, 'one_bedroom': 3200, 'two_bedroom': 4500, 'three_bedroom': 6000},
        'transit': {'subway_lines': ['2', '3', 'B', 'Q', 'F', 'G'], 'bus_routes': ['B61', 'B67'], 'nearest_station': '7th Ave', 'walk_score': 97, 'transit_score': 91},
        'safety': {'crime_index': 320, 'borough_avg_crime': 450, 'felony_count': 580, 'misdemeanor_count': 890},
        'amenities': {'schools_count': 18, 'hospitals_count': 2, 'parks_count': 10, 'grocery_stores_count': 18, 'restaurants_count': 55, 'pharmacies_count': 7},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 45, 'accessible_parks': 5, 'accessibility_notes': 'Good accessibility with Prospect Park'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 350, 'street_parking_available': False}
    },
    {
        'name': 'Williamsburg',
        'borough': 'Brooklyn',
        'latitude': 40.7081,
        'longitude': -73.9571,
        'description': 'Trendy neighborhood with hipster culture great food and waterfront views',
        'vibe': 'Lively',
        'rent': {'studio': 2200, 'one_bedroom': 3000, 'two_bedroom': 4200, 'three_bedroom': 5500},
        'transit': {'subway_lines': ['L', 'J', 'M', 'Z'], 'bus_routes': ['B24', 'B32', 'B60'], 'nearest_station': 'Bedford Ave', 'walk_score': 97, 'transit_score': 85},
        'safety': {'crime_index': 410, 'borough_avg_crime': 450, 'felony_count': 820, 'misdemeanor_count': 1150},
        'amenities': {'schools_count': 12, 'hospitals_count': 1, 'parks_count': 6, 'grocery_stores_count': 14, 'restaurants_count': 70, 'pharmacies_count': 6},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 35, 'accessible_parks': 3, 'accessibility_notes': 'Limited elevator access'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 400, 'street_parking_available': False}
    },
    {
        'name': 'Bushwick',
        'borough': 'Brooklyn',
        'latitude': 40.6944,
        'longitude': -73.9213,
        'description': 'Artsy neighborhood with vibrant nightlife and street art scene',
        'vibe': 'Lively',
        'rent': {'studio': 1600, 'one_bedroom': 2200, 'two_bedroom': 2900, 'three_bedroom': 3800},
        'transit': {'subway_lines': ['J', 'M', 'Z', 'L'], 'bus_routes': ['B13', 'B20', 'B26'], 'nearest_station': 'Myrtle-Wyckoff Aves', 'walk_score': 94, 'transit_score': 79},
        'safety': {'crime_index': 520, 'borough_avg_crime': 450, 'felony_count': 1100, 'misdemeanor_count': 1500},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 5, 'grocery_stores_count': 12, 'restaurants_count': 40, 'pharmacies_count': 4},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 25, 'accessible_parks': 2, 'accessibility_notes': 'Limited accessibility'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 200, 'street_parking_available': True}
    },
    {
        'name': 'Bay Ridge',
        'borough': 'Brooklyn',
        'latitude': 40.6349,
        'longitude': -74.0232,
        'description': 'Family friendly neighborhood with beautiful waterfront views and diverse community',
        'vibe': 'Quiet',
        'rent': {'studio': 1500, 'one_bedroom': 2000, 'two_bedroom': 2700, 'three_bedroom': 3500},
        'transit': {'subway_lines': ['R'], 'bus_routes': ['B1', 'B4', 'B37'], 'nearest_station': 'Bay Ridge Ave', 'walk_score': 88, 'transit_score': 65},
        'safety': {'crime_index': 280, 'borough_avg_crime': 450, 'felony_count': 420, 'misdemeanor_count': 680},
        'amenities': {'schools_count': 16, 'hospitals_count': 2, 'parks_count': 9, 'grocery_stores_count': 12, 'restaurants_count': 35, 'pharmacies_count': 6},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 30, 'accessible_parks': 4, 'accessibility_notes': 'Good park accessibility'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 180, 'street_parking_available': True}
    },
    {
        'name': 'Crown Heights',
        'borough': 'Brooklyn',
        'latitude': 40.6694,
        'longitude': -73.9421,
        'description': 'Diverse neighborhood with Caribbean culture and beautiful brownstones',
        'vibe': 'Mixed',
        'rent': {'studio': 1700, 'one_bedroom': 2300, 'two_bedroom': 3100, 'three_bedroom': 4000},
        'transit': {'subway_lines': ['2', '3', '4', '5'], 'bus_routes': ['B45', 'B46', 'B65'], 'nearest_station': 'Eastern Pkwy', 'walk_score': 93, 'transit_score': 82},
        'safety': {'crime_index': 450, 'borough_avg_crime': 450, 'felony_count': 920, 'misdemeanor_count': 1300},
        'amenities': {'schools_count': 14, 'hospitals_count': 2, 'parks_count': 7, 'grocery_stores_count': 13, 'restaurants_count': 42, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 38, 'accessible_parks': 3, 'accessibility_notes': 'Good subway accessibility'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 220, 'street_parking_available': True}
    },
    # QUEENS
    {
        'name': 'Astoria',
        'borough': 'Queens',
        'latitude': 40.7721,
        'longitude': -73.9302,
        'description': 'Vibrant neighborhood known for diverse food scene and easy Manhattan access',
        'vibe': 'Lively',
        'rent': {'studio': 1900, 'one_bedroom': 2600, 'two_bedroom': 3400, 'three_bedroom': 4200},
        'transit': {'subway_lines': ['N', 'W'], 'bus_routes': ['Q19', 'Q102', 'Q103'], 'nearest_station': 'Astoria-Ditmars Blvd', 'walk_score': 92, 'transit_score': 82},
        'safety': {'crime_index': 420, 'borough_avg_crime': 480, 'felony_count': 890, 'misdemeanor_count': 1200},
        'amenities': {'schools_count': 12, 'hospitals_count': 2, 'parks_count': 8, 'grocery_stores_count': 15, 'restaurants_count': 45, 'pharmacies_count': 6},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 42, 'accessible_parks': 4, 'accessibility_notes': 'Good ADA infrastructure'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 250, 'street_parking_available': True}
    },
    {
        'name': 'Jackson Heights',
        'borough': 'Queens',
        'latitude': 40.7557,
        'longitude': -73.8831,
        'description': 'Incredibly diverse neighborhood with amazing food from around the world',
        'vibe': 'Lively',
        'rent': {'studio': 1600, 'one_bedroom': 2100, 'two_bedroom': 2800, 'three_bedroom': 3500},
        'transit': {'subway_lines': ['7', 'E', 'F', 'M', 'R'], 'bus_routes': ['Q32', 'Q33', 'Q47'], 'nearest_station': 'Jackson Hts-Roosevelt Ave', 'walk_score': 98, 'transit_score': 88},
        'safety': {'crime_index': 380, 'borough_avg_crime': 480, 'felony_count': 780, 'misdemeanor_count': 1100},
        'amenities': {'schools_count': 14, 'hospitals_count': 2, 'parks_count': 6, 'grocery_stores_count': 20, 'restaurants_count': 60, 'pharmacies_count': 8},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 38, 'accessible_parks': 3, 'accessibility_notes': 'Major transit hub with good accessibility'},
        'parking': {'difficulty': 'Hard', 'avg_monthly_garage_cost': 200, 'street_parking_available': True}
    },
    {
        'name': 'Flushing',
        'borough': 'Queens',
        'latitude': 40.7675,
        'longitude': -73.8330,
        'description': 'Vibrant Asian community with amazing food and excellent transit connections',
        'vibe': 'Lively',
        'rent': {'studio': 1500, 'one_bedroom': 2000, 'two_bedroom': 2700, 'three_bedroom': 3400},
        'transit': {'subway_lines': ['7'], 'bus_routes': ['Q17', 'Q20A', 'Q44', 'Q58'], 'nearest_station': 'Flushing-Main St', 'walk_score': 96, 'transit_score': 80},
        'safety': {'crime_index': 360, 'borough_avg_crime': 480, 'felony_count': 720, 'misdemeanor_count': 1050},
        'amenities': {'schools_count': 16, 'hospitals_count': 2, 'parks_count': 7, 'grocery_stores_count': 22, 'restaurants_count': 65, 'pharmacies_count': 9},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 40, 'accessible_parks': 3, 'accessibility_notes': 'Main Street station fully accessible'},
        'parking': {'difficulty': 'Hard', 'avg_monthly_garage_cost': 180, 'street_parking_available': True}
    },
    {
        'name': 'Forest Hills',
        'borough': 'Queens',
        'latitude': 40.7196,
        'longitude': -73.8448,
        'description': 'Quiet suburban feel with excellent schools and beautiful Tudor style buildings',
        'vibe': 'Quiet',
        'rent': {'studio': 1700, 'one_bedroom': 2200, 'two_bedroom': 3000, 'three_bedroom': 4000},
        'transit': {'subway_lines': ['E', 'F', 'M', 'R'], 'bus_routes': ['Q23', 'Q60', 'Q10'], 'nearest_station': 'Forest Hills-71st Ave', 'walk_score': 90, 'transit_score': 78},
        'safety': {'crime_index': 260, 'borough_avg_crime': 480, 'felony_count': 380, 'misdemeanor_count': 620},
        'amenities': {'schools_count': 18, 'hospitals_count': 2, 'parks_count': 9, 'grocery_stores_count': 14, 'restaurants_count': 40, 'pharmacies_count': 7},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 42, 'accessible_parks': 5, 'accessibility_notes': 'Good accessibility throughout'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 160, 'street_parking_available': True}
    },
    {
        'name': 'Long Island City',
        'borough': 'Queens',
        'latitude': 40.7447,
        'longitude': -73.9485,
        'description': 'Up and coming neighborhood with Manhattan skyline views and new development',
        'vibe': 'Mixed',
        'rent': {'studio': 2100, 'one_bedroom': 2900, 'two_bedroom': 4000, 'three_bedroom': 5200},
        'transit': {'subway_lines': ['7', 'E', 'M', 'N', 'W'], 'bus_routes': ['Q67', 'Q69', 'Q103'], 'nearest_station': 'Queens Plaza', 'walk_score': 91, 'transit_score': 86},
        'safety': {'crime_index': 350, 'borough_avg_crime': 480, 'felony_count': 680, 'misdemeanor_count': 980},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 5, 'grocery_stores_count': 12, 'restaurants_count': 45, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 44, 'accessible_parks': 3, 'accessibility_notes': 'Modern buildings mostly accessible'},
        'parking': {'difficulty': 'Hard', 'avg_monthly_garage_cost': 300, 'street_parking_available': True}
    },
    # THE BRONX
    {
        'name': 'Riverdale',
        'borough': 'The Bronx',
        'latitude': 40.8901,
        'longitude': -73.9129,
        'description': 'Quiet residential neighborhood with suburban feel and great schools',
        'vibe': 'Quiet',
        'rent': {'studio': 1400, 'one_bedroom': 1900, 'two_bedroom': 2600, 'three_bedroom': 3200},
        'transit': {'subway_lines': ['1'], 'bus_routes': ['Bx10', 'Bx20', 'Bx34'], 'nearest_station': '231st Street', 'walk_score': 75, 'transit_score': 62},
        'safety': {'crime_index': 280, 'borough_avg_crime': 520, 'felony_count': 420, 'misdemeanor_count': 680},
        'amenities': {'schools_count': 15, 'hospitals_count': 3, 'parks_count': 12, 'grocery_stores_count': 10, 'restaurants_count': 25, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 28, 'accessible_parks': 6, 'accessibility_notes': 'Hilly terrain but good park accessibility'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 180, 'street_parking_available': True}
    },
    {
        'name': 'Fordham',
        'borough': 'The Bronx',
        'latitude': 40.8604,
        'longitude': -73.8978,
        'description': 'Bustling neighborhood near Fordham University with great transit access',
        'vibe': 'Lively',
        'rent': {'studio': 1200, 'one_bedroom': 1600, 'two_bedroom': 2200, 'three_bedroom': 2900},
        'transit': {'subway_lines': ['4', 'B', 'D'], 'bus_routes': ['Bx12', 'Bx17', 'Bx22'], 'nearest_station': 'Fordham Road', 'walk_score': 92, 'transit_score': 85},
        'safety': {'crime_index': 580, 'borough_avg_crime': 520, 'felony_count': 1200, 'misdemeanor_count': 1700},
        'amenities': {'schools_count': 16, 'hospitals_count': 3, 'parks_count': 6, 'grocery_stores_count': 12, 'restaurants_count': 35, 'pharmacies_count': 7},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 32, 'accessible_parks': 3, 'accessibility_notes': 'Good subway accessibility'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 150, 'street_parking_available': True}
    },
    {
        'name': 'Mott Haven',
        'borough': 'The Bronx',
        'latitude': 40.8085,
        'longitude': -73.9256,
        'description': 'Emerging arts neighborhood with affordable rents and easy Manhattan access',
        'vibe': 'Mixed',
        'rent': {'studio': 1100, 'one_bedroom': 1500, 'two_bedroom': 2000, 'three_bedroom': 2700},
        'transit': {'subway_lines': ['4', '5', '6'], 'bus_routes': ['Bx1', 'Bx2', 'Bx19'], 'nearest_station': '138th Street', 'walk_score': 88, 'transit_score': 80},
        'safety': {'crime_index': 620, 'borough_avg_crime': 520, 'felony_count': 1350, 'misdemeanor_count': 1900},
        'amenities': {'schools_count': 12, 'hospitals_count': 2, 'parks_count': 5, 'grocery_stores_count': 8, 'restaurants_count': 25, 'pharmacies_count': 4},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 28, 'accessible_parks': 2, 'accessibility_notes': 'Basic accessibility infrastructure'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 120, 'street_parking_available': True}
    },
    # STATEN ISLAND
    {
        'name': 'St. George',
        'borough': 'Staten Island',
        'latitude': 40.6437,
        'longitude': -74.0739,
        'description': 'Gateway to Staten Island with ferry access to Manhattan and affordable living',
        'vibe': 'Mixed',
        'rent': {'studio': 1200, 'one_bedroom': 1700, 'two_bedroom': 2300, 'three_bedroom': 2900},
        'transit': {'subway_lines': ['SIR'], 'bus_routes': ['S40', 'S44', 'S46', 'S52'], 'nearest_station': 'St. George Ferry', 'walk_score': 82, 'transit_score': 58},
        'safety': {'crime_index': 350, 'borough_avg_crime': 380, 'felony_count': 620, 'misdemeanor_count': 890},
        'amenities': {'schools_count': 10, 'hospitals_count': 2, 'parks_count': 8, 'grocery_stores_count': 8, 'restaurants_count': 20, 'pharmacies_count': 4},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 30, 'accessible_parks': 4, 'accessibility_notes': 'Ferry terminal fully accessible'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 120, 'street_parking_available': True}
    },
    {
        'name': 'Tottenville',
        'borough': 'Staten Island',
        'latitude': 40.5126,
        'longitude': -74.2518,
        'description': 'Quiet suburban neighborhood at the southern tip of Staten Island',
        'vibe': 'Quiet',
        'rent': {'studio': 1000, 'one_bedroom': 1400, 'two_bedroom': 1900, 'three_bedroom': 2500},
        'transit': {'subway_lines': ['SIR'], 'bus_routes': ['S74', 'S78'], 'nearest_station': 'Tottenville', 'walk_score': 55, 'transit_score': 35},
        'safety': {'crime_index': 180, 'borough_avg_crime': 380, 'felony_count': 180, 'misdemeanor_count': 320},
        'amenities': {'schools_count': 8, 'hospitals_count': 1, 'parks_count': 10, 'grocery_stores_count': 6, 'restaurants_count': 15, 'pharmacies_count': 3},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 20, 'accessible_parks': 5, 'accessibility_notes': 'Car dependent area'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 80, 'street_parking_available': True}
    },
]

# Additional 19 neighborhoods
ADDITIONAL_NEIGHBORHOODS = [
    # BROOKLYN
    {
        'name': 'Greenpoint',
        'borough': 'Brooklyn',
        'latitude': 40.7302,
        'longitude': -73.9519,
        'description': 'Trendy neighborhood with Polish heritage, waterfront views and artsy vibe',
        'vibe': 'Lively',
        'rent': {'studio': 2100, 'one_bedroom': 2900, 'two_bedroom': 4000, 'three_bedroom': 5200},
        'transit': {'subway_lines': ['G'], 'bus_routes': ['B43', 'B48', 'B62'], 'nearest_station': 'Greenpoint Ave', 'walk_score': 93, 'transit_score': 78},
        'safety': {'crime_index': 380, 'borough_avg_crime': 450, 'felony_count': 720, 'misdemeanor_count': 1050},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 6, 'grocery_stores_count': 12, 'restaurants_count': 55, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 32, 'accessible_parks': 3, 'accessibility_notes': 'Limited elevator access'},
        'parking': {'difficulty': 'Hard', 'avg_monthly_garage_cost': 350, 'street_parking_available': True}
    },
    {
        'name': 'Brooklyn Heights',
        'borough': 'Brooklyn',
        'latitude': 40.6960,
        'longitude': -73.9937,
        'description': 'Historic neighborhood with stunning Manhattan views and beautiful brownstones',
        'vibe': 'Quiet',
        'rent': {'studio': 2600, 'one_bedroom': 3500, 'two_bedroom': 5000, 'three_bedroom': 7000},
        'transit': {'subway_lines': ['2', '3', '4', '5', 'A', 'C', 'F'], 'bus_routes': ['B25', 'B26', 'B38'], 'nearest_station': 'Borough Hall', 'walk_score': 97, 'transit_score': 92},
        'safety': {'crime_index': 290, 'borough_avg_crime': 450, 'felony_count': 480, 'misdemeanor_count': 750},
        'amenities': {'schools_count': 12, 'hospitals_count': 2, 'parks_count': 8, 'grocery_stores_count': 14, 'restaurants_count': 45, 'pharmacies_count': 6},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 48, 'accessible_parks': 5, 'accessibility_notes': 'Good accessibility with Promenade'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 450, 'street_parking_available': False}
    },
    {
        'name': 'Fort Greene',
        'borough': 'Brooklyn',
        'latitude': 40.6896,
        'longitude': -73.9745,
        'description': 'Cultural neighborhood with arts scene Fort Greene Park and diverse community',
        'vibe': 'Mixed',
        'rent': {'studio': 2200, 'one_bedroom': 3000, 'two_bedroom': 4200, 'three_bedroom': 5500},
        'transit': {'subway_lines': ['B', 'D', 'N', 'Q', 'R', '2', '3', '4', '5'], 'bus_routes': ['B25', 'B38', 'B52'], 'nearest_station': 'Atlantic Ave-Barclays Ctr', 'walk_score': 96, 'transit_score': 90},
        'safety': {'crime_index': 380, 'borough_avg_crime': 450, 'felony_count': 720, 'misdemeanor_count': 1000},
        'amenities': {'schools_count': 14, 'hospitals_count': 2, 'parks_count': 7, 'grocery_stores_count': 13, 'restaurants_count': 50, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 42, 'accessible_parks': 4, 'accessibility_notes': 'Good transit accessibility'},
        'parking': {'difficulty': 'Hard', 'avg_monthly_garage_cost': 300, 'street_parking_available': True}
    },
    # BRONX
    {
        'name': 'Melrose',
        'borough': 'The Bronx',
        'latitude': 40.8196,
        'longitude': -73.9196,
        'description': 'Affordable South Bronx neighborhood with strong community and good transit',
        'vibe': 'Lively',
        'rent': {'studio': 1100, 'one_bedroom': 1500, 'two_bedroom': 2000, 'three_bedroom': 2600},
        'transit': {'subway_lines': ['2', '5'], 'bus_routes': ['Bx1', 'Bx2', 'Bx15'], 'nearest_station': 'Third Ave-149th St', 'walk_score': 90, 'transit_score': 82},
        'safety': {'crime_index': 580, 'borough_avg_crime': 520, 'felony_count': 1200, 'misdemeanor_count': 1700},
        'amenities': {'schools_count': 14, 'hospitals_count': 2, 'parks_count': 5, 'grocery_stores_count': 10, 'restaurants_count': 30, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 30, 'accessible_parks': 2, 'accessibility_notes': 'Basic accessibility infrastructure'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 120, 'street_parking_available': True}
    },
    {
        'name': 'Hunts Point',
        'borough': 'The Bronx',
        'latitude': 40.8157,
        'longitude': -73.8874,
        'description': 'Industrial neighborhood with strong community bonds and affordable living',
        'vibe': 'Mixed',
        'rent': {'studio': 1000, 'one_bedroom': 1400, 'two_bedroom': 1900, 'three_bedroom': 2500},
        'transit': {'subway_lines': ['6'], 'bus_routes': ['Bx6', 'Bx19', 'Bx39'], 'nearest_station': 'Hunts Point Ave', 'walk_score': 82, 'transit_score': 72},
        'safety': {'crime_index': 620, 'borough_avg_crime': 520, 'felony_count': 1350, 'misdemeanor_count': 1900},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 4, 'grocery_stores_count': 8, 'restaurants_count': 20, 'pharmacies_count': 3},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 22, 'accessible_parks': 2, 'accessibility_notes': 'Limited accessibility'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 100, 'street_parking_available': True}
    },
    {
        'name': 'Longwood',
        'borough': 'The Bronx',
        'latitude': 40.8229,
        'longitude': -73.9008,
        'description': 'Residential South Bronx neighborhood with improving amenities',
        'vibe': 'Mixed',
        'rent': {'studio': 1050, 'one_bedroom': 1450, 'two_bedroom': 1950, 'three_bedroom': 2600},
        'transit': {'subway_lines': ['2', '5'], 'bus_routes': ['Bx15', 'Bx19', 'Bx41'], 'nearest_station': 'Intervale Ave', 'walk_score': 86, 'transit_score': 76},
        'safety': {'crime_index': 560, 'borough_avg_crime': 520, 'felony_count': 1150, 'misdemeanor_count': 1650},
        'amenities': {'schools_count': 12, 'hospitals_count': 1, 'parks_count': 4, 'grocery_stores_count': 9, 'restaurants_count': 22, 'pharmacies_count': 4},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 25, 'accessible_parks': 2, 'accessibility_notes': 'Limited accessibility infrastructure'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 110, 'street_parking_available': True}
    },
    # MANHATTAN
    {
        'name': 'Financial District',
        'borough': 'Manhattan',
        'latitude': 40.7074,
        'longitude': -74.0113,
        'description': 'Historic lower Manhattan neighborhood with Wall Street and waterfront access',
        'vibe': 'Mixed',
        'rent': {'studio': 3000, 'one_bedroom': 4200, 'two_bedroom': 6000, 'three_bedroom': 8500},
        'transit': {'subway_lines': ['1', '2', '3', '4', '5', 'A', 'C', 'J', 'Z'], 'bus_routes': ['M5', 'M15', 'M20'], 'nearest_station': 'Fulton St', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 320, 'borough_avg_crime': 420, 'felony_count': 580, 'misdemeanor_count': 920},
        'amenities': {'schools_count': 8, 'hospitals_count': 2, 'parks_count': 5, 'grocery_stores_count': 10, 'restaurants_count': 70, 'pharmacies_count': 8},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 60, 'accessible_parks': 4, 'accessibility_notes': 'Excellent accessibility throughout'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 700, 'street_parking_available': False}
    },
    {
        'name': 'Tribeca',
        'borough': 'Manhattan',
        'latitude': 40.7163,
        'longitude': -74.0086,
        'description': 'Ultra trendy neighborhood with celebrity residents luxury lofts and great dining',
        'vibe': 'Quiet',
        'rent': {'studio': 4000, 'one_bedroom': 5500, 'two_bedroom': 8000, 'three_bedroom': 12000},
        'transit': {'subway_lines': ['1', '2', '3', 'A', 'C', 'E'], 'bus_routes': ['M20', 'M22'], 'nearest_station': 'Chambers St', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 250, 'borough_avg_crime': 420, 'felony_count': 380, 'misdemeanor_count': 620},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 4, 'grocery_stores_count': 8, 'restaurants_count': 80, 'pharmacies_count': 6},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 55, 'accessible_parks': 3, 'accessibility_notes': 'Good accessibility infrastructure'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 750, 'street_parking_available': False}
    },
    {
        'name': 'SoHo',
        'borough': 'Manhattan',
        'latitude': 40.7234,
        'longitude': -74.0018,
        'description': 'Famous shopping and art district with cast iron architecture and galleries',
        'vibe': 'Lively',
        'rent': {'studio': 3500, 'one_bedroom': 5000, 'two_bedroom': 7500, 'three_bedroom': 10000},
        'transit': {'subway_lines': ['A', 'C', 'E', '1', 'N', 'R', 'W'], 'bus_routes': ['M21', 'M6'], 'nearest_station': 'Spring St', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 280, 'borough_avg_crime': 420, 'felony_count': 450, 'misdemeanor_count': 750},
        'amenities': {'schools_count': 8, 'hospitals_count': 1, 'parks_count': 3, 'grocery_stores_count': 10, 'restaurants_count': 90, 'pharmacies_count': 7},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 58, 'accessible_parks': 2, 'accessibility_notes': 'Good ADA infrastructure'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 680, 'street_parking_available': False}
    },
    {
        'name': 'Greenwich Village',
        'borough': 'Manhattan',
        'latitude': 40.7336,
        'longitude': -74.0027,
        'description': 'Iconic bohemian neighborhood with NYU Washington Square Park and great dining',
        'vibe': 'Lively',
        'rent': {'studio': 3200, 'one_bedroom': 4500, 'two_bedroom': 6500, 'three_bedroom': 9000},
        'transit': {'subway_lines': ['A', 'B', 'C', 'D', 'E', 'F', 'M', '1', '2', '3'], 'bus_routes': ['M5', 'M6', 'M20'], 'nearest_station': 'W 4th St', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 300, 'borough_avg_crime': 420, 'felony_count': 520, 'misdemeanor_count': 850},
        'amenities': {'schools_count': 15, 'hospitals_count': 3, 'parks_count': 5, 'grocery_stores_count': 12, 'restaurants_count': 95, 'pharmacies_count': 9},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 62, 'accessible_parks': 4, 'accessibility_notes': 'Excellent accessibility'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 650, 'street_parking_available': False}
    },
    {
        'name': 'West Village',
        'borough': 'Manhattan',
        'latitude': 40.7358,
        'longitude': -74.0059,
        'description': 'Charming cobblestone streets with boutique shops cafes and historic townhouses',
        'vibe': 'Quiet',
        'rent': {'studio': 3400, 'one_bedroom': 4800, 'two_bedroom': 7000, 'three_bedroom': 10000},
        'transit': {'subway_lines': ['1', '2', '3', 'A', 'C', 'E'], 'bus_routes': ['M11', 'M14'], 'nearest_station': '14th St', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 260, 'borough_avg_crime': 420, 'felony_count': 400, 'misdemeanor_count': 680},
        'amenities': {'schools_count': 10, 'hospitals_count': 2, 'parks_count': 4, 'grocery_stores_count': 10, 'restaurants_count': 85, 'pharmacies_count': 7},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 58, 'accessible_parks': 3, 'accessibility_notes': 'Good ADA infrastructure'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 680, 'street_parking_available': False}
    },
    {
        'name': 'Chinatown',
        'borough': 'Manhattan',
        'latitude': 40.7158,
        'longitude': -73.9970,
        'description': 'Vibrant Asian community with authentic food markets and cultural heritage',
        'vibe': 'Lively',
        'rent': {'studio': 2200, 'one_bedroom': 3000, 'two_bedroom': 4200, 'three_bedroom': 5800},
        'transit': {'subway_lines': ['4', '5', '6', 'J', 'N', 'Q', 'R', 'W', 'Z'], 'bus_routes': ['M9', 'M15', 'M22'], 'nearest_station': 'Canal St', 'walk_score': 99, 'transit_score': 100},
        'safety': {'crime_index': 350, 'borough_avg_crime': 420, 'felony_count': 680, 'misdemeanor_count': 980},
        'amenities': {'schools_count': 12, 'hospitals_count': 2, 'parks_count': 4, 'grocery_stores_count': 20, 'restaurants_count': 100, 'pharmacies_count': 10},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 50, 'accessible_parks': 3, 'accessibility_notes': 'Good transit accessibility'},
        'parking': {'difficulty': 'Very Hard', 'avg_monthly_garage_cost': 580, 'street_parking_available': False}
    },
    # QUEENS
    {
        'name': 'Queensbridge',
        'borough': 'Queens',
        'latitude': 40.7544,
        'longitude': -73.9434,
        'description': 'Neighborhood near Long Island City with easy Manhattan access',
        'vibe': 'Mixed',
        'rent': {'studio': 1800, 'one_bedroom': 2400, 'two_bedroom': 3200, 'three_bedroom': 4200},
        'transit': {'subway_lines': ['E', 'F', 'M', 'N', 'W'], 'bus_routes': ['Q67', 'Q69'], 'nearest_station': 'Queens Plaza', 'walk_score': 88, 'transit_score': 84},
        'safety': {'crime_index': 420, 'borough_avg_crime': 480, 'felony_count': 850, 'misdemeanor_count': 1200},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 5, 'grocery_stores_count': 10, 'restaurants_count': 30, 'pharmacies_count': 4},
        'accessibility': {'has_elevator_station': True, 'ada_intersections': 38, 'accessible_parks': 3, 'accessibility_notes': 'Good transit accessibility'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 220, 'street_parking_available': True}
    },
    {
        'name': 'Woodside',
        'borough': 'Queens',
        'latitude': 40.7448,
        'longitude': -73.9019,
        'description': 'Diverse neighborhood with Irish and Asian communities and great transit',
        'vibe': 'Mixed',
        'rent': {'studio': 1600, 'one_bedroom': 2100, 'two_bedroom': 2800, 'three_bedroom': 3600},
        'transit': {'subway_lines': ['7'], 'bus_routes': ['Q18', 'Q19', 'Q38'], 'nearest_station': 'Woodside-61st St', 'walk_score': 90, 'transit_score': 82},
        'safety': {'crime_index': 360, 'borough_avg_crime': 480, 'felony_count': 700, 'misdemeanor_count': 1000},
        'amenities': {'schools_count': 12, 'hospitals_count': 1, 'parks_count': 5, 'grocery_stores_count': 14, 'restaurants_count': 40, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 34, 'accessible_parks': 3, 'accessibility_notes': 'Limited elevator access'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 180, 'street_parking_available': True}
    },
    {
        'name': 'Elmhurst',
        'borough': 'Queens',
        'latitude': 40.7367,
        'longitude': -73.8790,
        'description': 'One of the most diverse neighborhoods in the world with amazing food',
        'vibe': 'Lively',
        'rent': {'studio': 1500, 'one_bedroom': 2000, 'two_bedroom': 2700, 'three_bedroom': 3400},
        'transit': {'subway_lines': ['M', 'R'], 'bus_routes': ['Q29', 'Q53', 'Q58'], 'nearest_station': 'Elmhurst Ave', 'walk_score': 92, 'transit_score': 78},
        'safety': {'crime_index': 380, 'borough_avg_crime': 480, 'felony_count': 750, 'misdemeanor_count': 1100},
        'amenities': {'schools_count': 14, 'hospitals_count': 2, 'parks_count': 6, 'grocery_stores_count': 20, 'restaurants_count': 60, 'pharmacies_count': 8},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 36, 'accessible_parks': 3, 'accessibility_notes': 'Limited elevator access'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 160, 'street_parking_available': True}
    },
    {
        'name': 'Ridgewood',
        'borough': 'Queens',
        'latitude': 40.7057,
        'longitude': -73.9038,
        'description': 'Up and coming neighborhood on Brooklyn Queens border with great food scene',
        'vibe': 'Mixed',
        'rent': {'studio': 1700, 'one_bedroom': 2300, 'two_bedroom': 3100, 'three_bedroom': 4000},
        'transit': {'subway_lines': ['L', 'M'], 'bus_routes': ['B13', 'Q55', 'Q58'], 'nearest_station': 'Fresh Pond Rd', 'walk_score': 91, 'transit_score': 76},
        'safety': {'crime_index': 360, 'borough_avg_crime': 480, 'felony_count': 700, 'misdemeanor_count': 1000},
        'amenities': {'schools_count': 12, 'hospitals_count': 1, 'parks_count': 6, 'grocery_stores_count': 14, 'restaurants_count': 45, 'pharmacies_count': 5},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 32, 'accessible_parks': 3, 'accessibility_notes': 'Limited accessibility'},
        'parking': {'difficulty': 'Moderate', 'avg_monthly_garage_cost': 170, 'street_parking_available': True}
    },
    {
        'name': 'Bayside',
        'borough': 'Queens',
        'latitude': 40.7632,
        'longitude': -73.7696,
        'description': 'Quiet suburban neighborhood with waterfront access and excellent schools',
        'vibe': 'Quiet',
        'rent': {'studio': 1600, 'one_bedroom': 2100, 'two_bedroom': 2900, 'three_bedroom': 3800},
        'transit': {'subway_lines': ['LIRR'], 'bus_routes': ['Q12', 'Q13', 'Q31'], 'nearest_station': 'Bayside LIRR', 'walk_score': 72, 'transit_score': 52},
        'safety': {'crime_index': 220, 'borough_avg_crime': 480, 'felony_count': 320, 'misdemeanor_count': 550},
        'amenities': {'schools_count': 18, 'hospitals_count': 2, 'parks_count': 10, 'grocery_stores_count': 12, 'restaurants_count': 35, 'pharmacies_count': 6},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 35, 'accessible_parks': 5, 'accessibility_notes': 'Car dependent area'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 140, 'street_parking_available': True}
    },
    # STATEN ISLAND
    {
        'name': 'Stapleton',
        'borough': 'Staten Island',
        'latitude': 40.6279,
        'longitude': -74.0746,
        'description': 'Waterfront neighborhood with ferry access and growing arts community',
        'vibe': 'Mixed',
        'rent': {'studio': 1100, 'one_bedroom': 1500, 'two_bedroom': 2100, 'three_bedroom': 2700},
        'transit': {'subway_lines': ['SIR'], 'bus_routes': ['S74', 'S76', 'S78'], 'nearest_station': 'Stapleton SIR', 'walk_score': 72, 'transit_score': 48},
        'safety': {'crime_index': 380, 'borough_avg_crime': 380, 'felony_count': 680, 'misdemeanor_count': 980},
        'amenities': {'schools_count': 8, 'hospitals_count': 1, 'parks_count': 6, 'grocery_stores_count': 7, 'restaurants_count': 18, 'pharmacies_count': 3},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 22, 'accessible_parks': 3, 'accessibility_notes': 'Basic accessibility'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 100, 'street_parking_available': True}
    },
    {
        'name': 'Port Richmond',
        'borough': 'Staten Island',
        'latitude': 40.6368,
        'longitude': -74.1341,
        'description': 'Historic neighborhood with Latino community and affordable housing',
        'vibe': 'Mixed',
        'rent': {'studio': 1000, 'one_bedroom': 1400, 'two_bedroom': 1900, 'three_bedroom': 2500},
        'transit': {'subway_lines': ['SIR'], 'bus_routes': ['S40', 'S44', 'S48'], 'nearest_station': 'St George Ferry', 'walk_score': 68, 'transit_score': 42},
        'safety': {'crime_index': 360, 'borough_avg_crime': 380, 'felony_count': 640, 'misdemeanor_count': 920},
        'amenities': {'schools_count': 7, 'hospitals_count': 1, 'parks_count': 5, 'grocery_stores_count': 8, 'restaurants_count': 15, 'pharmacies_count': 3},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 18, 'accessible_parks': 2, 'accessibility_notes': 'Car dependent area'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 90, 'street_parking_available': True}
    },
    {
        'name': 'New Dorp',
        'borough': 'Staten Island',
        'latitude': 40.5732,
        'longitude': -74.1189,
        'description': 'Suburban neighborhood with shopping district and good schools',
        'vibe': 'Quiet',
        'rent': {'studio': 1100, 'one_bedroom': 1500, 'two_bedroom': 2000, 'three_bedroom': 2600},
        'transit': {'subway_lines': ['SIR'], 'bus_routes': ['S54', 'S57', 'S59'], 'nearest_station': 'New Dorp SIR', 'walk_score': 62, 'transit_score': 38},
        'safety': {'crime_index': 220, 'borough_avg_crime': 380, 'felony_count': 300, 'misdemeanor_count': 520},
        'amenities': {'schools_count': 10, 'hospitals_count': 1, 'parks_count': 7, 'grocery_stores_count': 8, 'restaurants_count': 20, 'pharmacies_count': 4},
        'accessibility': {'has_elevator_station': False, 'ada_intersections': 20, 'accessible_parks': 4, 'accessibility_notes': 'Car dependent suburban area'},
        'parking': {'difficulty': 'Easy', 'avg_monthly_garage_cost': 85, 'street_parking_available': True}
    },
]


class Command(BaseCommand):
    help = 'Seed database with 39 real NYC neighborhoods'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS(
                '🗽 Starting NestMapper NYC data seeding...'
            )
        )

        created = 0
        updated = 0
        errors = 0

        all_neighborhoods = NEIGHBORHOODS_DATA + ADDITIONAL_NEIGHBORHOODS

        for data in all_neighborhoods:
            try:
                neighborhood, is_new = Neighborhood.objects.update_or_create(
                    name=data['name'],
                    borough=data['borough'],
                    defaults={
                        'latitude': data['latitude'],
                        'longitude': data['longitude'],
                        'description': data['description'],
                        'vibe': data['vibe'],
                    }
                )

                RentData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['rent']
                )

                TransitInfo.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['transit']
                )

                SafetyData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['safety']
                )

                Amenities.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['amenities']
                )

                AccessibilityData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['accessibility']
                )

                ParkingData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['parking']
                )

                if is_new:
                    created += 1
                    self.stdout.write(
                        f'✅ Created: {neighborhood.name}, {neighborhood.borough}'
                    )
                else:
                    updated += 1
                    self.stdout.write(
                        f'🔄 Updated: {neighborhood.name}, {neighborhood.borough}'
                    )

            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(
                        f'❌ Error with {data["name"]}: {e}'
                    )
                )

        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Done! Created: {created}, Updated: {updated}, Errors: {errors}'
        ))
        self.stdout.write(
            self.style.SUCCESS(
                'Now run: python manage.py compute_scores'
            )
        )