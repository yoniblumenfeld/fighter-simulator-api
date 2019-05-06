from rest_framework import serializers
from .models import UserProfile,Fighter
from rest_framework.response import Response

INITIAL_STAMINA=10
INITIAL_SPEED=10
INITIAL_STRENGTH=10
INITIAL_EXPERIENCE=0

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes UserProfile objects"""
    class Meta:
        model = UserProfile
        fields = ('id','email','name','password','money','date_created')
        extra_kwargs = {'password':{'write_only':True},'date_created':{'read_only':True}}

    def create(self,validated_data):
        """Creates and returns a new user object"""
        user = UserProfile(
            email=validated_data['email'],
            name=validated_data['name'],
            money=100
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def update(self, instance, validated_data):
        super().update(instance,validated_data)
        if "password" in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class FighterSerializer(serializers.ModelSerializer):
    """Serializes Fighter objects"""
    class Meta:
        model = Fighter
        fields = ('id','name','user_profile','martial_art','stamina','strength','speed','experience')

    def create(self, validated_data):
        fighter = Fighter(
            name=validated_data["name"],
            experience=INITIAL_EXPERIENCE,
            stamina=INITIAL_STAMINA,
            speed=INITIAL_SPEED,
            strength=INITIAL_STRENGTH,
            martial_art=validated_data["martial_art"]
        )
        fighter.user_profile = self.context["request"].user
        fighter.save()
        return fighter

    def validate_name(self,name):
        """Making sure users don't have fighters with the same name on creation"""
        user = self.context["request"].user
        fighter_name_in_db = len(user.fighter_set.filter(name=name))
        if not self.instance:
            if fighter_name_in_db > 0:
                raise serializers.ValidationError("User already has a fighter with that name")
        return name

    def validate_strength(self, value):
        if value > 100:
            raise serializers.ValidationError("Strength exceeds 100")
        return value

    def validate_speed(self, value):
        if value > 100:
            raise serializers.ValidationError("Speed exceeds 100")
        return value

    def validate_stamina(self, value):
        if value > 100:
            raise serializers.ValidationError("Stamina exceeds 100")
        return value
