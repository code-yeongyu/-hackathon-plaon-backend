import json

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.authtoken import views as drf_views

from drf_yasg.utils import swagger_auto_schema
import drf_yasg.openapi as openapi

from custom_profile.forms import SignUpForm
from custom_profile.models import Profile
from custom_profile.serializers import ProfileSerializer


@swagger_auto_schema(method='post',
                     operation_description="Resgiter a new account",
                     responses={
                         201: 'Account Created Successfully',
                         406: 'Errors occured with given datas'
                     },
                     manual_parameters=SignUpForm.Meta.parameters)
@api_view(['POST'])
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
    permission_classes = (permissions.IsAuthenticated, )

    queryset = Profile.objects.all()

    @swagger_auto_schema(
        operation_description="Get the informations of requested user",
        responses={200: 'Successfully returned the requested value.'},
        manual_parameters=ProfileSerializer.Meta.parameters)
    def get(self, request):
        profile = Profile.objects.get(user=request.user)
        return Response(ProfileSerializer(profile).data,
                        status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Update the informations of requested user",
        responses={
            200: 'Successfully updated the requested value.',
            406: 'Errors occured with given datas'
        },
        manual_parameters=[
            ProfileSerializer.Meta.parameters[0],
        ])
    def patch(self, request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors,
                        status=status.HTTP_406_NOT_ACCEPTABLE)


class GetAuthToken(drf_views.ObtainAuthToken):
    @swagger_auto_schema(operation_description="Get token of requested user",
                         responses={
                             200: 'Successfully updated the requested value.',
                         },
                         manual_parameters=[
                             openapi.Parameter('username',
                                               openapi.IN_QUERY,
                                               description="username",
                                               type=openapi.TYPE_STRING),
                             openapi.Parameter('password',
                                               openapi.IN_QUERY,
                                               description="password",
                                               type=openapi.FORMAT_PASSWORD),
                         ])
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})