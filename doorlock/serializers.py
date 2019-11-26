from rest_framework import serializers

import drf_yasg.openapi as openapi

from doorlock.models import Doorlock


class DoorlockSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    beacon_id = serializers.ReadOnlyField()
    push_id = serializers.ReadOnlyField()

    class Meta:
        model = Doorlock
        fields = ('owner', 'beacon_id', 'push_id', 'location_text', 'nickname')
        parameters = [
            openapi.Parameter('owner',
                              openapi.IN_QUERY,
                              description="username of owner",
                              type=openapi.TYPE_STRING),  # not for patch
            openapi.Parameter('beacon_id',
                              openapi.IN_QUERY,
                              description="beacon id",
                              type=openapi.TYPE_NUMBER),  # not for patch
            openapi.Parameter('push_id',
                              openapi.IN_QUERY,
                              description="push id",
                              type=openapi.TYPE_NUMBER),  # not for patch
            openapi.Parameter('location_text',
                              openapi.IN_QUERY,
                              description="location text",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('nickname',
                              openapi.IN_QUERY,
                              description="nickname",
                              type=openapi.TYPE_STRING),
        ]