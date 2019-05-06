from django.db import models
from django.contrib.auth import validators
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin

class UserProfileManager(BaseUserManager):
    """Reconfiguring Django's base user manager for
    our custom user model."""

    def create_user(self, email, name, password=None):
        """Creates a new user profile object."""
        if not email:
            raise ValueError("Users must have an email address!")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,name,password=None):
        """Creates a new superuser profile object."""
        superuser = self.create_user(email,name,password)
        superuser.is_staff = True
        superuser.is_superuser = True
        superuser.save(using=self._db)
        return superuser

class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Represents a user profile inside our system"""
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    money = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Used to get a users full name."""
        return self.name

    def get_short_name(self):
        """Used to get a users short name."""

        return self.name

    def __str__(self):
        """Used when converting user object to string"""
        return "User(email={},name={},money={})".format(self.email, self.name, self.money)

    class Meta:
        ordering = ('date_created',)

class Fighter(models.Model):
    """Represents a fighter in our system"""
    name = models.CharField(max_length=255)
    martial_art = models.CharField(max_length=255)
    stamina = models.IntegerField(default=10)
    strength = models.IntegerField(default=10)
    speed = models.IntegerField(default=10)
    experience = models.FloatField(default=10.0)
    user_profile = models.ForeignKey("UserProfile",on_delete=models.CASCADE,null=True)
    safe_traits = ['stamina','strength','speed','experience']
    def __str__(self):
        """returns objects as astring"""
        return "exp: {} name: {}\nstamina: {}\nstrength: {}\nspeed: {}\nmartial art: {}".format(
            self.experience,self.name,self.stamina,self.strength,self.speed,self.martial_art
        )

    def train(self,trait,price):
        """
        Train a trait.
        returns current trait level if training succeed (if user has enough money)
        returns -1 if training didnt work (not enoguh money or illegal trait)
        """
        if trait in Fighter.safe_traits:
            if self.user_profile.money - price >= 0:
                self.user_profile.money -= price
                self.__setattr__(trait,self.__getattribute__(trait)+price)
                return self.__getattribute__(trait)
        return -1



