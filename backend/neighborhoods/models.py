from django.db import models


class Neighborhood(models.Model):
    """
    Main table — every other table links to this.
    Stores the basic info about each neighborhood.
    """
    BOROUGH_CHOICES = [
        ('Manhattan', 'Manhattan'),
        ('Brooklyn', 'Brooklyn'),
        ('Queens', 'Queens'),
        ('The Bronx', 'The Bronx'),
        ('Staten Island', 'Staten Island'),
    ]

    VIBE_CHOICES = [
        ('Quiet', 'Quiet'),
        ('Lively', 'Lively'),
        ('Mixed', 'Mixed'),
    ]

    name = models.CharField(max_length=100)
    borough = models.CharField(
        max_length=50,
        choices=BOROUGH_CHOICES
    )
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(blank=True)
    vibe = models.CharField(
        max_length=20,
        choices=VIBE_CHOICES,
        default='Mixed'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name}, {self.borough}"

    class Meta:
        ordering = ['borough', 'name']


class RentData(models.Model):
    """
    Stores average monthly rent for each
    neighborhood in USD.
    """
    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='rent'
    )
    studio = models.IntegerField(help_text="Average studio rent in USD")
    one_bedroom = models.IntegerField(help_text="Average 1BR rent in USD")
    two_bedroom = models.IntegerField(help_text="Average 2BR rent in USD")
    three_bedroom = models.IntegerField(
        help_text="Average 3BR rent in USD",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Rent data for {self.neighborhood.name}"


class TransitInfo(models.Model):
    """
    Stores subway lines, bus routes and
    walkability for each neighborhood.
    """
    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='transit'
    )
    subway_lines = models.JSONField(
        default=list,
        help_text="List of subway lines e.g ['A','C','E']"
    )
    bus_routes = models.JSONField(
        default=list,
        help_text="List of bus routes e.g ['M15','M79']"
    )
    nearest_station = models.CharField(max_length=100)
    walk_score = models.IntegerField(
        help_text="Walkability score 0-100"
    )
    transit_score = models.IntegerField(
        help_text="Transit score 0-100"
    )

    def __str__(self):
        return f"Transit data for {self.neighborhood.name}"


class SafetyData(models.Model):
    """
    Stores crime statistics for each
    neighborhood from NYC Open Data.
    """
    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='safety'
    )
    crime_index = models.FloatField(
        help_text="Raw crime index from NYC Open Data"
    )
    borough_avg_crime = models.FloatField(
        help_text="Borough average crime index for comparison"
    )
    felony_count = models.IntegerField(
        help_text="Annual felony count",
        null=True,
        blank=True
    )
    misdemeanor_count = models.IntegerField(
        help_text="Annual misdemeanor count",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Safety data for {self.neighborhood.name}"


class Amenities(models.Model):
    """
    Stores counts of nearby essential
    services within half mile radius.
    """
    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='amenities'
    )
    schools_count = models.IntegerField(default=0)
    hospitals_count = models.IntegerField(default=0)
    parks_count = models.IntegerField(default=0)
    grocery_stores_count = models.IntegerField(default=0)
    restaurants_count = models.IntegerField(default=0)
    pharmacies_count = models.IntegerField(default=0)

    def __str__(self):
        return f"Amenities for {self.neighborhood.name}"


class AccessibilityData(models.Model):
    """
    Stores disability accessibility info.
    This is our UNIQUE feature — no other
    tool covers this for NYC neighborhoods.
    """
    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='accessibility'
    )
    has_elevator_station = models.BooleanField(
        default=False,
        help_text="Does nearest subway station have elevator?"
    )
    ada_intersections = models.IntegerField(
        default=0,
        help_text="Number of ADA compliant intersections"
    )
    accessible_parks = models.IntegerField(
        default=0,
        help_text="Number of wheelchair accessible parks"
    )
    accessibility_notes = models.TextField(
        blank=True,
        help_text="Any additional accessibility information"
    )

    def __str__(self):
        return f"Accessibility data for {self.neighborhood.name}"


class ParkingData(models.Model):
    """
    Stores parking difficulty and cost.
    Important for car owners choosing
    a neighborhood to live in.
    """
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Hard', 'Hard'),
        ('Very Hard', 'Very Hard'),
    ]

    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='parking'
    )
    difficulty = models.CharField(
        max_length=20,
        choices=DIFFICULTY_CHOICES,
        default='Moderate'
    )
    avg_monthly_garage_cost = models.IntegerField(
        help_text="Average monthly garage cost in USD",
        null=True,
        blank=True
    )
    street_parking_available = models.BooleanField(default=True)
    parking_notes = models.TextField(blank=True)

    def __str__(self):
        return f"Parking data for {self.neighborhood.name}"


class NeighborhoodScore(models.Model):
    """
    Stores the computed scores for each
    neighborhood. This table is populated
    by running our scoring algorithm.
    All scores are on a scale of 1 to 10.
    """
    neighborhood = models.OneToOneField(
        Neighborhood,
        on_delete=models.CASCADE,
        related_name='scores'
    )
    affordability_score = models.FloatField(default=0)
    transit_score = models.FloatField(default=0)
    safety_score = models.FloatField(default=0)
    family_score = models.FloatField(default=0)
    accessibility_score = models.FloatField(default=0)
    convenience_score = models.FloatField(default=0)
    overall_score = models.FloatField(default=0)
    last_computed = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Scores for {self.neighborhood.name}"