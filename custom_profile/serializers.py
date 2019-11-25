from rest_framework import serializers

import drf_yasg.openapi as openapi

from custom_profile.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    accessible_beacon_id = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ('name', 'accessible_beacon_id')
        parameters = [
            openapi.Parameter('name',
                              openapi.IN_QUERY,
                              description="name",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('accessible_beacon_id',
                              openapi.IN_QUERY,
                              description="JSON typed integer array",
                              type="JSON typed-array"),
        ]