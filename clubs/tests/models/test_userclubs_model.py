"""Unit tests for the Club model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import UserClubs, User, Club
from django.utils import timezone

#Create your tests here
class UserClubModelTestCase(TestCase):
    """Unit tests for the UserClubs model."""

    fixtures = ["clubs/tests/fixtures/users.json", "clubs/tests/fixtures/clubs.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.club = Club.objects.get(name = 'ClubB')
        self.is_applicant = True
        self.is_member = False
        self.is_owner = False
        self.is_officer = False
    
    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_xp_cannot_be_less_than_zero(self):
        self.user.chess_xp = -1
        self._assert_user_is_invalid()

    def test_first_name_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_first_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.first_name = second_user.first_name
        self._assert_user_is_valid()

    def test_first_name_may_contain_50_characters(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_first_name_must_not_contain_more_than_50_characters(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()


    def test_last_name_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_last_name_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.last_name = second_user.last_name
        self._assert_user_is_valid()

    def test_last_name_may_contain_50_characters(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_last_name_must_not_contain_more_than_50_characters(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()

    def test_personal_statement_must_not_contain_more_than_1000_characters(self):
        self.user.last_name = 'x' * 1001
        self._assert_user_is_invalid()


    def test_username_must_not_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()

    def test_username_must_be_unique(self):
        second_user = self._create_second_user()
        self.user.username = second_user.username
        self._assert_user_is_invalid()


    def test_username_must_contain_at_symbol(self):
        self.user.username = 'johndoe.example.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_domain_name(self):
        self.user.username = 'johndoe@.org'
        self._assert_user_is_invalid()

    def test_username_must_contain_domain(self):
        self.user.username = 'johndoe@example'
        self._assert_user_is_invalid()

    def test_username_must_not_contain_more_than_one_at(self):
        self.user.username = 'johndoe@@example.org'
        self._assert_user_is_invalid()


    def test_bio_may_be_blank(self):
        self.user.bio = ''
        self._assert_user_is_valid()

    def test_statement_may_be_blank(self):
        self.user.statement = ''
        self._assert_user_is_invalid()

    def test_bio_need_not_be_unique(self):
        second_user = self._create_second_user()
        self.user.bio = second_user.bio
        self._assert_user_is_valid()

    def test_bio_may_contain_520_characters(self):
        self.user.bio = 'x' * 520
        self._assert_user_is_valid()

    def test_bio_must_not_contain_more_than_520_characters(self):
        self.user.bio = 'x' * 521
        self._assert_user_is_invalid()

    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail('Test user should be valid')

    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()

    def _create_second_user(self):
        second_user = User.objects.get(username = 'janedoe1@example.org')
        return second_user

    def test_valid_club(self):
        self._assert_club_is_valid()

    def test_club_name_must_not_be_blank(self):
        self.club.name = ''
        self._assert_club_is_invalid()

    def test_description_may_contain_520_characters(self):
        self.club.description = 'x' * 520
        self._assert_club_is_valid()

    def test_description_must_not_contain_more_than_520_characters(self):
        self.club.description = 'x' * 521
        self._assert_club_is_invalid()

    def test_location_can_be_blank(self):
        self.club.description = ''
        self._assert_club_is_valid()

    def test_location_may_contain_20_characters(self):
        self.club.location = 'x' * 20
        self._assert_club_is_valid()

    def test_location_must_not_contain_more_than_20_characters(self):
        self.club.location = 'x' * 21
        self._assert_club_is_invalid()

    def test_location_must_not_be_blank(self):
        self.club.location = ''
        self._assert_club_is_invalid()

    def test_club_name_must_not_be_blank(self):
        self.club.name = ''
        self._assert_club_is_invalid()

    # def test_club_name_must_be_unique(self):
    #     second_club = self._create_second_club()
    #     self.club.name = second_club.name
    #     self._assert_club_is_invalid()

    def _assert_club_is_valid(self):
        try:
            self.club.full_clean()
        except (ValidationError):
            self.fail('Test club should be valid')

    def _assert_club_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.club.full_clean()

    def _create_second_club(self):
        second_club = Club.objects.get(name = 'Club2')
        return second_club