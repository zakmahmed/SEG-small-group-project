"""Unit tests for the Club model."""
from django.core.exceptions import ValidationError
from django.test import TestCase
from clubs.models import Membership, User, Club
from django.utils import timezone

class MembershipTestCase(TestCase):
    """Unit tests for the Membership model."""

    fixtures = ["clubs/tests/fixtures/users.json", "clubs/tests/fixtures/clubs.json"]

    def setUp(self):
        self.user = User.objects.get(username = 'janedoe@example.org')
        self.other_user = User.objects.get(username = 'janedoe1@example.org')
        self.club = Club.objects.get(name = 'TheGrand')
        self.owner = Membership(user = self.user, club = self.club, is_applicant = True, is_member = True, is_officer = True, is_owner = True)
        self.owner.save()
        self.other_member = Membership(user = self.other_user, club = self.club, is_applicant = True, is_member = True)
        self.other_member.save()

    def test_promote_member(self):
        beforeOfficer = self.other_member.is_officer
        self.owner.promote_member(self.other_member)
        afterOfficer = self.other_member.is_officer
        self.assertFalse(beforeOfficer)
        self.assertTrue(afterOfficer)

    def test_demote_officer(self):
        self.other_member.is_officer = True
        beforeOfficer = self.other_member.is_officer
        self.owner.demote_officer(self.other_member)
        afterOfficer = self.other_member.is_officer
        self.assertTrue(beforeOfficer)
        self.assertFalse(afterOfficer)

    def test_transfer_ownership(self):
        beforeOwner = self.owner.is_owner
        beforeOtherMemberOwner = self.other_member.is_owner
        self.owner.transfer_ownership(self.other_member)
        afterOwner = self.owner.is_owner
        afterOtherMemberOwner = self.other_member.is_owner
        self.assertTrue(beforeOwner)
        self.assertFalse(beforeOtherMemberOwner)
        self.assertFalse(afterOwner)
        self.assertTrue(afterOtherMemberOwner)

    def test_approve_application(self):
        self.other_member.is_member = False
        beforeMember = self.other_member.is_member
        self.owner.approve_application(self.other_member)
        afterMember = self.other_member.is_member
        self.assertFalse(beforeMember)
        self.assertTrue(afterMember)

    def test_reject_application(self):
        self.other_member.is_member = False
        beforeCount = Membership.objects.count()
        self.owner.reject_application(self.other_member)
        afterCount = Membership.objects.count()
        self.assertEqual(beforeCount, afterCount + 1)

    def test_reject_application_for_a_member(self):
        beforeCount = Membership.objects.count()
        self.owner.reject_application(self.other_member)
        afterCount = Membership.objects.count()
        self.assertEqual(beforeCount, afterCount)

    def test_on_delete_user(self):
        beforeCount = Membership.objects.count()
        self.user.delete()
        afterCount = Membership.objects.count()
        self.assertEqual(beforeCount, afterCount + 1)

    def test_on_delete_club(self):
        beforeCount = Membership.objects.count()
        self.club.delete()
        afterCount = Membership.objects.count()
        self.assertEqual(beforeCount, afterCount + 2)
