from rest_framework import serializers
from .models import Category, Nomination, Preference, Vote


class CategorySerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Category
        fields = '__all__'


class NominationSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Nomination
        fields = '__all__'


class PreferenceSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Preference
        fields = '__all__'


class VoteSerializer(serializers.ModelSerializer):
    user=serializers.ReadOnlyField(source="user.username")
    class Meta:
        model = Vote
        fields = '__all__'
