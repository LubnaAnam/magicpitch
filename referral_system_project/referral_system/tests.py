from django.test import TestCase

# Create your tests here.
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserTests(APITestCase):
    def test_user_registration(self):
        url = reverse('user-registration')
        data = {'username': 'testuser', 'email': 'test8@example.com', 'password': 'testpass'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_details(self):
        user = User.objects.create(username='testuser', email='test@example.com', password='testpass')
        self.client.force_authenticate(user=user)
        url = reverse('user-details')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_referrals(self):
        user = User.objects.create(username='testuser', email='test@example.com', password='testpass', referral_code='ref123')
        self.client.force_authenticate(user=user)
        url = reverse('referrals')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# abc