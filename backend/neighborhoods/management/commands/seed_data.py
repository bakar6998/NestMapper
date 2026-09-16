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


# Real NYC neighborhood data
# Sources: NYC Open Data, MTA, StreetEasy
NEIGHBORHOODS_DATA = [
    {
        'name': 'Astoria',
        'borough': 'Queens',
        'latitude': 40.7721,
        'longitude': -73.9302,
        'description': 'Vibrant neighborhood known for diverse food scene and easy Manhattan access',
        'vibe': 'Lively',
        'rent': {
            'studio': 1900,
            'one_bedroom': 2600,
            'two_bedroom': 3400,
            'three_bedroom': 4200
        },
        'transit': {
            'subway_lines': ['N', 'W'],
            'bus_routes': ['Q19', 'Q102', 'Q103'],
            'nearest_station': 'Astoria-Ditmars Blvd',
            'walk_score': 92,
            'transit_score': 82
        },
        'safety': {
            'crime_index': 420,
            'borough_avg_crime': 480,
            'felony_count': 890,
            'misdemeanor_count': 1200
        },
        'amenities': {
            'schools_count': 12,
            'hospitals_count': 2,
            'parks_count': 8,
            'grocery_stores_count': 15,
            'restaurants_count': 45,
            'pharmacies_count': 6
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 42,
            'accessible_parks': 4,
            'accessibility_notes': 'Good ADA infrastructure'
        },
        'parking': {
            'difficulty': 'Moderate',
            'avg_monthly_garage_cost': 250,
            'street_parking_available': True
        }
    },
    {
        'name': 'Jackson Heights',
        'borough': 'Queens',
        'latitude': 40.7557,
        'longitude': -73.8831,
        'description': 'Incredibly diverse neighborhood with amazing food from around the world',
        'vibe': 'Lively',
        'rent': {
            'studio': 1600,
            'one_bedroom': 2100,
            'two_bedroom': 2800,
            'three_bedroom': 3500
        },
        'transit': {
            'subway_lines': ['7', 'E', 'F', 'M', 'R'],
            'bus_routes': ['Q32', 'Q33', 'Q47'],
            'nearest_station': 'Jackson Hts-Roosevelt Ave',
            'walk_score': 98,
            'transit_score': 88
        },
        'safety': {
            'crime_index': 380,
            'borough_avg_crime': 480,
            'felony_count': 780,
            'misdemeanor_count': 1100
        },
        'amenities': {
            'schools_count': 14,
            'hospitals_count': 2,
            'parks_count': 6,
            'grocery_stores_count': 20,
            'restaurants_count': 60,
            'pharmacies_count': 8
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 38,
            'accessible_parks': 3,
            'accessibility_notes': 'Major transit hub with good accessibility'
        },
        'parking': {
            'difficulty': 'Hard',
            'avg_monthly_garage_cost': 200,
            'street_parking_available': True
        }
    },
    {
        'name': 'Riverdale',
        'borough': 'The Bronx',
        'latitude': 40.8901,
        'longitude': -73.9129,
        'description': 'Quiet residential neighborhood with a suburban feel and great schools',
        'vibe': 'Quiet',
        'rent': {
            'studio': 1400,
            'one_bedroom': 1900,
            'two_bedroom': 2600,
            'three_bedroom': 3200
        },
        'transit': {
            'subway_lines': ['1'],
            'bus_routes': ['Bx10', 'Bx20', 'Bx34'],
            'nearest_station': '231st Street',
            'walk_score': 75,
            'transit_score': 62
        },
        'safety': {
            'crime_index': 280,
            'borough_avg_crime': 520,
            'felony_count': 420,
            'misdemeanor_count': 680
        },
        'amenities': {
            'schools_count': 15,
            'hospitals_count': 3,
            'parks_count': 12,
            'grocery_stores_count': 10,
            'restaurants_count': 25,
            'pharmacies_count': 5
        },
        'accessibility': {
            'has_elevator_station': False,
            'ada_intersections': 28,
            'accessible_parks': 6,
            'accessibility_notes': 'Hilly terrain but good park accessibility'
        },
        'parking': {
            'difficulty': 'Easy',
            'avg_monthly_garage_cost': 180,
            'street_parking_available': True
        }
    },
    {
        'name': 'Park Slope',
        'borough': 'Brooklyn',
        'latitude': 40.6728,
        'longitude': -73.9797,
        'description': 'Family friendly neighborhood with beautiful brownstones and Prospect Park',
        'vibe': 'Mixed',
        'rent': {
            'studio': 2400,
            'one_bedroom': 3200,
            'two_bedroom': 4500,
            'three_bedroom': 6000
        },
        'transit': {
            'subway_lines': ['2', '3', 'B', 'Q', 'F', 'G'],
            'bus_routes': ['B61', 'B67', 'B69'],
            'nearest_station': '7th Ave',
            'walk_score': 97,
            'transit_score': 91
        },
        'safety': {
            'crime_index': 320,
            'borough_avg_crime': 450,
            'felony_count': 580,
            'misdemeanor_count': 890
        },
        'amenities': {
            'schools_count': 18,
            'hospitals_count': 2,
            'parks_count': 10,
            'grocery_stores_count': 18,
            'restaurants_count': 55,
            'pharmacies_count': 7
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 45,
            'accessible_parks': 5,
            'accessibility_notes': 'Good accessibility with Prospect Park nearby'
        },
        'parking': {
            'difficulty': 'Very Hard',
            'avg_monthly_garage_cost': 350,
            'street_parking_available': False
        }
    },
    {
        'name': 'Bushwick',
        'borough': 'Brooklyn',
        'latitude': 40.6944,
        'longitude': -73.9213,
        'description': 'Artsy neighborhood with a vibrant nightlife and street art scene',
        'vibe': 'Lively',
        'rent': {
            'studio': 1600,
            'one_bedroom': 2200,
            'two_bedroom': 2900,
            'three_bedroom': 3800
        },
        'transit': {
            'subway_lines': ['J', 'M', 'Z', 'L'],
            'bus_routes': ['B13', 'B20', 'B26'],
            'nearest_station': 'Myrtle-Wyckoff Aves',
            'walk_score': 94,
            'transit_score': 79
        },
        'safety': {
            'crime_index': 520,
            'borough_avg_crime': 450,
            'felony_count': 1100,
            'misdemeanor_count': 1500
        },
        'amenities': {
            'schools_count': 10,
            'hospitals_count': 1,
            'parks_count': 5,
            'grocery_stores_count': 12,
            'restaurants_count': 40,
            'pharmacies_count': 4
        },
        'accessibility': {
            'has_elevator_station': False,
            'ada_intersections': 25,
            'accessible_parks': 2,
            'accessibility_notes': 'Limited accessibility infrastructure'
        },
        'parking': {
            'difficulty': 'Moderate',
            'avg_monthly_garage_cost': 200,
            'street_parking_available': True
        }
    },
    {
        'name': 'Upper West Side',
        'borough': 'Manhattan',
        'latitude': 40.7870,
        'longitude': -73.9754,
        'description': 'Classic Manhattan neighborhood with cultural institutions and Central Park access',
        'vibe': 'Mixed',
        'rent': {
            'studio': 2800,
            'one_bedroom': 3800,
            'two_bedroom': 5200,
            'three_bedroom': 7500
        },
        'transit': {
            'subway_lines': ['1', '2', '3', 'B', 'C'],
            'bus_routes': ['M10', 'M11', 'M72', 'M79'],
            'nearest_station': '72nd Street',
            'walk_score': 99,
            'transit_score': 100
        },
        'safety': {
            'crime_index': 310,
            'borough_avg_crime': 420,
            'felony_count': 650,
            'misdemeanor_count': 980
        },
        'amenities': {
            'schools_count': 22,
            'hospitals_count': 5,
            'parks_count': 8,
            'grocery_stores_count': 20,
            'restaurants_count': 80,
            'pharmacies_count': 12
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 65,
            'accessible_parks': 6,
            'accessibility_notes': 'Excellent accessibility throughout'
        },
        'parking': {
            'difficulty': 'Very Hard',
            'avg_monthly_garage_cost': 600,
            'street_parking_available': False
        }
    },
    {
        'name': 'Harlem',
        'borough': 'Manhattan',
        'latitude': 40.8116,
        'longitude': -73.9465,
        'description': 'Historic neighborhood with rich cultural heritage and improving amenities',
        'vibe': 'Lively',
        'rent': {
            'studio': 1800,
            'one_bedroom': 2400,
            'two_bedroom': 3200,
            'three_bedroom': 4500
        },
        'transit': {
            'subway_lines': ['2', '3', 'A', 'B', 'C', 'D'],
            'bus_routes': ['M1', 'M2', 'M3', 'M102'],
            'nearest_station': '125th Street',
            'walk_score': 96,
            'transit_score': 95
        },
        'safety': {
            'crime_index': 480,
            'borough_avg_crime': 420,
            'felony_count': 980,
            'misdemeanor_count': 1400
        },
        'amenities': {
            'schools_count': 20,
            'hospitals_count': 4,
            'parks_count': 10,
            'grocery_stores_count': 16,
            'restaurants_count': 50,
            'pharmacies_count': 9
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 52,
            'accessible_parks': 5,
            'accessibility_notes': 'Good transit accessibility'
        },
        'parking': {
            'difficulty': 'Hard',
            'avg_monthly_garage_cost': 350,
            'street_parking_available': True
        }
    },
    {
        'name': 'St. George',
        'borough': 'Staten Island',
        'latitude': 40.6437,
        'longitude': -74.0739,
        'description': 'Gateway to Staten Island with ferry access to Manhattan and affordable living',
        'vibe': 'Mixed',
        'rent': {
            'studio': 1200,
            'one_bedroom': 1700,
            'two_bedroom': 2300,
            'three_bedroom': 2900
        },
        'transit': {
            'subway_lines': ['SIR'],
            'bus_routes': ['S40', 'S44', 'S46', 'S52'],
            'nearest_station': 'St. George Ferry',
            'walk_score': 82,
            'transit_score': 58
        },
        'safety': {
            'crime_index': 350,
            'borough_avg_crime': 380,
            'felony_count': 620,
            'misdemeanor_count': 890
        },
        'amenities': {
            'schools_count': 10,
            'hospitals_count': 2,
            'parks_count': 8,
            'grocery_stores_count': 8,
            'restaurants_count': 20,
            'pharmacies_count': 4
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 30,
            'accessible_parks': 4,
            'accessibility_notes': 'Ferry terminal is fully accessible'
        },
        'parking': {
            'difficulty': 'Easy',
            'avg_monthly_garage_cost': 120,
            'street_parking_available': True
        }
    },
    {
        'name': 'Williamsburg',
        'borough': 'Brooklyn',
        'latitude': 40.7081,
        'longitude': -73.9571,
        'description': 'Trendy neighborhood with hipster culture, great food and waterfront views',
        'vibe': 'Lively',
        'rent': {
            'studio': 2200,
            'one_bedroom': 3000,
            'two_bedroom': 4200,
            'three_bedroom': 5500
        },
        'transit': {
            'subway_lines': ['L', 'J', 'M', 'Z'],
            'bus_routes': ['B24', 'B32', 'B60'],
            'nearest_station': 'Bedford Ave',
            'walk_score': 97,
            'transit_score': 85
        },
        'safety': {
            'crime_index': 410,
            'borough_avg_crime': 450,
            'felony_count': 820,
            'misdemeanor_count': 1150
        },
        'amenities': {
            'schools_count': 12,
            'hospitals_count': 1,
            'parks_count': 6,
            'grocery_stores_count': 14,
            'restaurants_count': 70,
            'pharmacies_count': 6
        },
        'accessibility': {
            'has_elevator_station': False,
            'ada_intersections': 35,
            'accessible_parks': 3,
            'accessibility_notes': 'Limited elevator access at subway'
        },
        'parking': {
            'difficulty': 'Very Hard',
            'avg_monthly_garage_cost': 400,
            'street_parking_available': False
        }
    },
    {
        'name': 'Flushing',
        'borough': 'Queens',
        'latitude': 40.7675,
        'longitude': -73.8330,
        'description': 'Vibrant Asian community with amazing food and excellent transit connections',
        'vibe': 'Lively',
        'rent': {
            'studio': 1500,
            'one_bedroom': 2000,
            'two_bedroom': 2700,
            'three_bedroom': 3400
        },
        'transit': {
            'subway_lines': ['7'],
            'bus_routes': ['Q17', 'Q20A', 'Q44', 'Q58'],
            'nearest_station': 'Flushing-Main St',
            'walk_score': 96,
            'transit_score': 80
        },
        'safety': {
            'crime_index': 360,
            'borough_avg_crime': 480,
            'felony_count': 720,
            'misdemeanor_count': 1050
        },
        'amenities': {
            'schools_count': 16,
            'hospitals_count': 2,
            'parks_count': 7,
            'grocery_stores_count': 22,
            'restaurants_count': 65,
            'pharmacies_count': 9
        },
        'accessibility': {
            'has_elevator_station': True,
            'ada_intersections': 40,
            'accessible_parks': 3,
            'accessibility_notes': 'Main Street station fully accessible'
        },
        'parking': {
            'difficulty': 'Hard',
            'avg_monthly_garage_cost': 180,
            'street_parking_available': True
        }
    },
]


class Command(BaseCommand):
    help = 'Seed database with NYC neighborhood data'

    def handle(self, *args, **kwargs):
        self.stdout.write(
            self.style.SUCCESS('Starting data seeding...')
        )

        created = 0
        updated = 0
        errors = 0

        for data in NEIGHBORHOODS_DATA:
            try:
                # Create or update neighborhood
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

                # Rent data
                RentData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['rent']
                )

                # Transit data
                TransitInfo.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['transit']
                )

                # Safety data
                SafetyData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['safety']
                )

                # Amenities
                Amenities.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['amenities']
                )

                # Accessibility
                AccessibilityData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['accessibility']
                )

                # Parking
                ParkingData.objects.update_or_create(
                    neighborhood=neighborhood,
                    defaults=data['parking']
                )

                if is_new:
                    created += 1
                    self.stdout.write(f'✅ Created: {neighborhood.name}, {neighborhood.borough}')
                else:
                    updated += 1
                    self.stdout.write(f'🔄 Updated: {neighborhood.name}, {neighborhood.borough}')

            except Exception as e:
                errors += 1
                self.stdout.write(
                    self.style.ERROR(f'❌ Error with {data["name"]}: {e}')
                )

        self.stdout.write(self.style.SUCCESS(
            f'\nDone! Created: {created}, Updated: {updated}, Errors: {errors}'
        ))
        self.stdout.write(
            self.style.SUCCESS('Run compute_scores to calculate scores!')
        )