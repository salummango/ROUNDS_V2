from rest_framework import serializers
from .models import User,Team
from django.contrib.auth.hashers import make_password

# class UserSerializer(serializers.ModelSerializer):
#     userImage = serializers.ImageField(required=True)
#     class Meta:
#         model = User  
#         fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phoneNo','userImage']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.password = make_password(password)  # Using make_password to hash the password
#         instance.save()
#         return instance


# serializers.py
from rest_framework import serializers
from .models import User, Team

class TeamSerializer(serializers.ModelSerializer):
    TeamLogo=serializers.ImageField(required=True)
    class Meta:
        model = Team
        fields = ['id', 'TeamName', 'TeamStadium', 'TeamCity','TeamLogo']

class UserSerializer(serializers.ModelSerializer):
    userImage = serializers.ImageField(required=True)
    
    team = TeamSerializer()  # Nested serializer for Team
    
    class Meta:
        model = User  
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'phoneNo', 'userImage', 'team']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        team_data = validated_data.pop('team')  # Extracting team data
        team = Team.objects.create(**team_data)
        validated_data['team'] = team  # Assigning team instance
        password = validated_data.pop('password', None)
        if password is not None:
            validated_data['password'] = make_password(password)  # Hashing the password
        return super().create(validated_data)

    def update(self, instance, validated_data):
        team_data = validated_data.pop('team', {})  # Extracting team data
        if team_data:
            team = instance.team
            team.TeamName = team_data.get('TeamName', team.TeamName)
            team.TeamStadium = team_data.get('TeamStadium', team.TeamStadium)
            team.TeamCity = team_data.get('TeamCity', team.TeamCity)
            team.save()
        password = validated_data.pop('password', None)
        if password:
            instance.password = make_password(password)
        return super().update(instance, validated_data)



