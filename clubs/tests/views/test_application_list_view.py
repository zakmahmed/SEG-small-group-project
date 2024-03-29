from django.conf import settings
from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Club, Membership
from clubs.tests.helpers import reverse_with_next

class ApplicationListTest(TestCase):

    fixtures = ['clubs/tests/fixtures/clubs.json', 'clubs/tests/fixtures/users.json']

    def setUp(self):
        self.club = Club.objects.get(name = 'TheGrand')
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.user2 = User.objects.get(username = 'janedoe1@example.org')
        self.club_user = Membership.objects.create(
        user = self.user,
        club = self.club,
        is_applicant = True,
        is_member = True,
        is_officer = True,
        is_owner = True
        )
        self.club_user.save()
        self.club_user2 = Membership.objects.create(
        user = self.user2,
        club = self.club,
        is_applicant = True,
        is_member = True,
        is_officer = False,
        is_owner = False
        )
        self.club_user2.save()
        self.club2 = Club.objects.get(name = 'ClubB')
        Membership(user = self.user, club = self.club2, is_applicant = True, is_member = True, is_officer = True, is_owner = True).save()
        self.url = reverse('application_list', kwargs = {'club_name': self.club.name})

    def test_application_list_url(self):
        self.assertEqual(self.url,f'/application_list/{self.club.name}/')

    def test_get_application_list(self):
        self.client.login(username=self.user.username, password='Password123')
        self._create_test_applicants(5)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application_list.html')
        for user_id in range(5):
            self.assertContains(response, f'user{user_id}@example.org')
            self.assertContains(response, f'First{user_id}')
            self.assertContains(response, f'Last{user_id}')
            self.assertContains(response, f'Bio{user_id}')
            self.assertContains(response, f'Statement{user_id}')
            self.assertContains(response, f'Chess experience: {user_id}')

    def test_empty_application_list(self):
        self.client.login(username=self.user.username, password='Password123')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'application_list.html')
        self.assertContains(response, 'No applications')

    def test_get_application_list_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_get_application_list_redirects_when_user_is_not_officer_owner(self):
        self.client.login(username=self.user2.username, password='Password123')
        response = self.client.get(self.url)
        redirect_url = reverse('access_denied')
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def _create_test_applicants(self, user_count=5):
        for user_id in range(user_count):
            self.user = User.objects.create_user(
                f'user{user_id}@example.org',
                password='Password123',
                first_name=f'First{user_id}',
                last_name=f'Last{user_id}',
                bio=f'Bio{user_id}',
                statement = f'Statement{user_id}',
                chess_xp = user_id
            )
            self.club_user = Membership.objects.create(
            user = self.user,
            club = self.club,
            is_applicant = True
            )
            self.club_user.save()
