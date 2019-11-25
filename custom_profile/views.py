import json

from rest_framework import permissions, status
from rest_framework.response import Response

from custom_profile.forms import SignUpForm
from custom_profile.models import Profile
from custom_profile.serializers import ProfileSerializer


def register(request):  # 회원가입
    form = SignUpForm(request.POST)
    if form.is_valid():
        user = form.save(commit=False)
        user.save()
        profile = Profile.objects.get(user=user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        return Response(status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)


class ProfileAPIView(APIView):
    """
        Profile
        ---
        # Content
            - name: CharField(max_length=10, null=True): name field
            - accessible_beacon_id: TextField(blank=True, Null=False, default="[]"): json string field
    """
    permission_classes = (permissions.IsAuthenticated, )

    # queryset = Profile.objects.all()

    def get(self, request):  # 프로필 조회
        profile = Profile.objects.get(user=request.user)
        return Response(ProfileSerializer(profile).data,
                        status=status.HTTP_200_OK)

    def patch(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)