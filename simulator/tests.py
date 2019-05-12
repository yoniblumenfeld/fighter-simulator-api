from django.test import TestCase
from rest_framework.test import APIClient
from profiles_api.models import UserProfile,Fighter
from rest_framework import status
import json

class TestSimulation(TestCase):
    def setUp(self):
        self.request = APIClient()
        self.test_user1 = UserProfile.objects.create_user(
            "test1@test.com",
            "testuser1",
            "test123"
        )
        self.test_user2 = UserProfile.objects.create_user(
            "test2@test.com",
            "testuser2",
            "test123"
        )
        self.user_1_fighter = Fighter.objects.create(
            name="user1fighter",
            stamina=10,
            strength=10,
            speed=10,
            martial_art="kravmaga"
        )
        self.user_1_fighter.user_profile = self.test_user1
        self.user_1_fighter.save()
        self.test_user1.save()
        self.user_2_fighter = Fighter.objects.create(
            name="user2fighter",
            stamina=15,
            strength=10,
            speed=10,
            martial_art="kungfu"
        )
        self.user_2_fighter.user_profile = self.test_user2
        self.user_2_fighter.save()
        self.test_user2.save()

    def test_simualtion_success(self):
        """
        checks whether the fight simulation returns successful result
        and doesnt raise errors
        """
        self.request.force_authenticate(user=self.test_user1)
        simulation_data = {
            "user_fighter_id":self.user_1_fighter.id,
            "opponent_id":self.test_user2.id,
            "opponent_fighter_id":self.user_2_fighter.id
        }
        res = self.request.post("http://127.0.0.1:8000/simulator/simulate/",json.dumps(simulation_data),content_type="application/json")
        self.assertEqual(status.HTTP_200_OK,res.status_code)


    def tearDown(self):
        self.user_2_fighter.delete()
        self.user_1_fighter.delete()
        self.test_user1.delete()
        self.test_user2.delete()