from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, UserClubs
from clubs.tests.helpers import reverse_with_next

class Club_Profile_Test(TestCase):

    fixtures = [
        'clubs/tests/fixtures/default_user.json',
        'clubs/tests/fixtures/clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='janedoe@example.org')
        self.club = Club.objects.get(name = "TheGrand")
        self.user_club = UserClubs.objects.create(user = self.user, club = self.club, is_member = True, is_officer = True, is_owner = True)
        self.url = reverse('club_profile', kwargs={'club_name': self.club.name})

    def test_show_user_url(self):
        self.assertEqual(self.url,f'/club_profile/{self.club.name}/')

    def test_get_show_club_profile_with_valid_user(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_users(10)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'club_profile.html')
        self.assertContains(response, "TheGrand")
        self.assertContains(response, "The best")
        self.assertContains(response, "London")
        self.assertContains(response, "Jane Doe")
        self.assertContains(response, "My bio")
        self.assertContains(response, "Number of members: 11")
        
    def _create_test_users(self, user_count = 10):
        for user_id in range(user_count):
            self.user2 = User.objects.create_user(
                f'user{user_id}@example.org',
                password='Password123',
                first_name='First',
                last_name='Last',
                bio='Bio',
                statement = 'Statement',
                chess_xp = 10,
            )
            self.club_user = UserClubs(user = self.user2, club = self.club, is_member = True)
            self.club_user.save()

    def test_get_club_profile_with_invalid_club(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('club_profile', kwargs={'club_name': self.club.name + "Not a club"})
        response = self.client.get(url, follow=True)
        response_url = reverse('club_list')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'club_list.html')

    def test_get_club_profile_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)
