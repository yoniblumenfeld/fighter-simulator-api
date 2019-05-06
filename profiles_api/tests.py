from django.test import TestCase
from rest_framework.test import APIClient,force_authenticate
from .models import UserProfile,Fighter
from rest_framework import status

class ProfileTests(TestCase):
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

    def test_list_all_users(self):
        """
        Checks whether the result objects contain user1's and user2's emails or not
        Thus implicating whether the url returns proper result.
        """
        res = self.request.get("http://127.0.0.1:8000/profile/",format="json")
        self.assertEqual([self.test_user1.email,self.test_user2.email],[user.get("email") for user in res.data])

    def test_list_current_user(self):
        """
        Check whether the response object data has user1's email in it.
        Thus implicating whether the url returns proper result.
        """
        res = self.request.get("http://127.0.0.1:8000/profile/1/",format="json")
        self.assertEqual(self.test_user1.email,res.data.get("email"))

    def test_create_user(self):
        """Checks whether a user is being created"""
        temp_user = {
            "email":"temp@temp.com",
            "name":"tempname",
            "password":"123456!a"
        }
        res = self.request.post("http://127.0.0.1:8000/profile/",temp_user)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_login(self):
        """Checks whether login works"""
        creds = {"username":self.test_user1.email,"password":"test123"}
        self.assertTrue(self.request.login(username=creds["username"],password=creds["password"]))

    def test_partial_update_user(self):
        """Checks whether a user is being updated successfully with patch http method"""
        new_email = {"email":"newemail@email.com"}
        self.request.force_authenticate(user=self.test_user1)
        res = self.request.patch("http://127.0.0.1:8000/profile/1/",new_email)
        self.assertEqual(status.HTTP_200_OK,res.status_code)

    def test_update_user(self):
        """Checks whether a user is being updated successfully with put http method"""
        new_email = {"email":"newemail@email.com","password":self.test_user1.password,"name":self.test_user1.name}
        self.request.force_authenticate(user=self.test_user1)
        res = self.request.put("http://127.0.0.1:8000/profile/1/",new_email)
        self.assertTrue(res.status_code == status.HTTP_200_OK)

    def test_delete_user(self):
        """Tests UserProfile deletion"""
        self.request.force_authenticate(user=self.test_user1)
        res = self.request.delete("http://127.0.0.1:8000/profile/1/")
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def tearDown(self):
        self.test_user2.delete()
        self.test_user1.delete()

class FighterTests(TestCase):
    def setUp(self):
        self.request = APIClient()
        self.test_user = UserProfile.objects.create_user(
            "test@test.com",
            "testuser",
            "test123"
        )
        self.fighter = Fighter.objects.create(
            name="test_fighter",
            martial_art="kungfu",
            stamina=10,
            strength=10,
            speed=10,
            experience=10.0,
            user_profile=self.test_user
        )
        self.request.force_authenticate(user=self.test_user)

    def test_create_fighter(self):
        """
        Tests if fighter is created with proper parameters
        """
        test_fighter = {
            "name":"testfighter1",
            "martial_art":"thaibox"
        }
        res = self.request.post("http://127.0.0.1:8000/fighter/",test_fighter)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)

    def test_partial_update_fighter(self):
        """
        Tests if fighter updates partially
        with patch http method
        """
        test_update = {
            "stamina":"56"
        }
        prev_stamina = self.fighter.stamina
        res = self.request.patch("http://127.0.0.1:8000/fighter/1/",test_update)
        self.assertFalse(res.data.get("stamina") == prev_stamina)

    def test_update_fighter(self):
        """
        Tests if fighter updates fully
        with put http method
        """
        test_update = {
            "name":"newname",
            "martial_art":self.fighter.martial_art
        }
        prev_name = self.fighter.name
        res = self.request.put("http://127.0.0.1:8000/fighter/1/",test_update)
        self.assertFalse(res.data.get("name") == prev_name)

    def test_delete_fighter(self):
        """
        Test if fighter deletes
        with delete http method
        """
        res = self.request.delete("http://127.0.0.1:8000/fighter/1/")
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def tearDown(self):
        self.test_user.delete()
        self.fighter.delete()