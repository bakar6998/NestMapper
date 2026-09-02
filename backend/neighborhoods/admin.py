from django.contrib import admin
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

admin.site.register(Neighborhood)
admin.site.register(RentData)
admin.site.register(TransitInfo)
admin.site.register(SafetyData)
admin.site.register(Amenities)
admin.site.register(AccessibilityData)
admin.site.register(ParkingData)
admin.site.register(NeighborhoodScore)
