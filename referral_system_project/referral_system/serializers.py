from rest_framework import serializers
from .models import User
from .models import Referral, User


# REGISTRATION
class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'referral_code']
        extra_kwargs = {'password': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user




#USER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'referral_code', 'date_joined']






#REFERRAL
class ReferralSerializer(serializers.ModelSerializer):
    referred_user = serializers.StringRelatedField()
    class Meta:
        model = Referral
        fields = ['referred_user', 'timestamp']
