from django.db import transaction
from rest_framework import serializers

from user.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','password']
        depth = 1

    @transaction.atomic()
    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        # check if user already exists or not
        #if not created then it creates the user
        user = User.objects.get_or_create(username=username)
        if not user[1]:
            # if the user details already exists,
            raise serializers.ValidationError('User already exist. Please login or try a different username')
            
        # password
        user[0].set_password(password)
        user[0].save()
        return user[0]
