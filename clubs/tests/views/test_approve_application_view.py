from django.test import TestCase
from django.urls import reverse
from clubs.models import User, Membership, Club
from clubs.tests.helpers import reverse_with_next

class ApproveApplicationTest(TestCase):

    fixtures = [
        'clubs/tests/fixtures/users.json',
        'clubs/tests/fixtures/clubs.json'
    ]

    def setUp(self):
        self.user = User.objects.get(username='janedoe@example.org')
        self.other_user = User.objects.get(username='janedoe1@example.org')
        self.club = Club.objects.get(name = "TheGrand")
        self.club_user = Membership(user = self.user ,club = self.club, is_applicant = True, is_member = True, is_officer = True, is_owner = True)
        self.club_user.save()
        self.other_member = Membership(user = self.other_user ,club = self.club, is_applicant = True)
        self.other_member.save()
        self.url = reverse('approve_application', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id})

    def test_approve_application_url(self):
        self.assertEqual(self.url,f'/approve_application/{self.other_member.club.name}/{self.other_user.id}')

    def test_get_approve_application_redirects_when_not_logged_in(self):
        redirect_url = reverse_with_next('log_in', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(response, redirect_url, status_code=302, target_status_code=200)

    def test_approve_application_who_is_not_member(self):
        self.client.login(username=self.user.username, password='Password123')
        is_member_before = self.other_member.is_member
        self.club_user.approve_application(self.other_member)
        response = self.client.get(self.url, follow=True)
        is_member_after = self.other_member.is_member
        self.assertFalse(is_member_before)
        self.assertTrue(is_member_after)
        response_url = reverse('application_list', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'application_list.html')

    def test_approve_application_who_is_already_member(self):
        self.client.login(username=self.user.username, password='Password123')
        self.other_member.is_member = True
        is_member_before = self.other_member.is_member
        self.club_user.approve_application(self.other_member)
        response = self.client.get(self.url, follow=True)
        is_member_after = self.other_member.is_member
        self.assertTrue(is_member_before)
        self.assertTrue(is_member_after)
        response_url = reverse('application_list', kwargs={'club_name': self.other_member.club.name})
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'application_list.html')

    def test_approve_application_not_as_officer_or_owner(self):
        self.club_user.is_officer = False
        self.club_user.is_owner = False
        self.club_user.save()
        self.client.login(username=self.user.username, password='Password123')
        is_member_before = self.other_member.is_member
        response = self.client.get(self.url, follow=True)
        is_member_after = self.other_member.is_member
        self.assertFalse(is_member_before)
        self.assertFalse(is_member_after)
        response_url = reverse('access_denied')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'access_denied.html')

    def test_get_approve_application_with_invalid_id(self):
        self.client.login(username=self.user.username, password='Password123')
        url = reverse('approve_application', kwargs={'club_name': self.other_member.club.name, 'user_id': self.other_user.id+9999})
        response = self.client.get(url, follow=True)
        response_url = reverse('my_clubs')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'my_clubs.html')
