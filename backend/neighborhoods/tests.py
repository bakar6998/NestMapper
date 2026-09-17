from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Neighborhood


class NeighborhoodAPITest(APITestCase):
    """
    Tests for all API endpoints
    Runs automatically on every push
    via GitHub Actions CI/CD
    """

    def setUp(self):
        """
        Creates test data before each test
        """
        self.neighborhood = Neighborhood.objects.create(
            name='Test Neighborhood',
            borough='Queens',
            latitude=40.7721,
            longitude=-73.9302,
            description='Test description',
            vibe='Lively'
        )

    def test_get_all_neighborhoods(self):
        """
        Test GET /api/neighborhoods/
        Should return 200 and list
        """
        url = reverse('all-neighborhoods')
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print('✅ GET /api/neighborhoods/ works!')

    def test_get_neighborhood_detail(self):
        """
        Test GET /api/neighborhoods/1/
        Should return 200 with data
        """
        url = reverse(
            'neighborhood-detail',
            args=[self.neighborhood.id]
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            response.data['name'],
            'Test Neighborhood'
        )
        print('✅ GET /api/neighborhoods/id/ works!')

    def test_get_neighborhood_not_found(self):
        """
        Test GET /api/neighborhoods/999/
        Should return 404
        """
        url = reverse(
            'neighborhood-detail',
            args=[999]
        )
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND
        )
        print('✅ 404 handling works!')

    def test_search_neighborhoods(self):
        """
        Test GET /api/search/?q=Test
        Should return results
        """
        url = '/api/search/?q=Test'
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print('✅ GET /api/search/ works!')

    def test_get_recommendations(self):
        """
        Test POST /api/recommend/
        Should return 200
        """
        url = reverse('recommendations')
        data = {
            'budget': 2000,
            'transit_priority': 3,
            'has_children': False,
            'needs_accessibility': False,
            'has_car': False
        }
        response = self.client.post(
            url, data, format='json'
        )
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print('✅ POST /api/recommend/ works!')

    def test_compare_neighborhoods(self):
        """
        Test GET /api/compare/?ids=1,1
        Should return 200
        """
        url = f'/api/compare/?ids={self.neighborhood.id},{self.neighborhood.id}'
        response = self.client.get(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        print('✅ GET /api/compare/ works!')