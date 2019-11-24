from rest_framework import serializers
from custom_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('name', 'accessible_beacon_id')