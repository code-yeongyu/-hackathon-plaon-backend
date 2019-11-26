from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.decorators import api_view

from doorlock.models import Doorlock
from doorlock.forms import DoorlockCreationForm
from doorlock.serializers import DoorlockSerializer


class DoorlockOverall(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            doorlocks = Doorlock.objects.filter(owner=request.user).values()
            return Response(doorlocks, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        if request.user.is_authenticated:
            serializer = DoorlockSerializer(data=request.data)
            form = DoorlockCreationForm(request.POST)
            if serializer.is_valid() and form.is_valid():
                serializer.save(
                    owner=request.user,
                    beacon_id=request.data.get('beacon_id'),
                    push_id=request.data.get('push_id'),
                )  # 작성자 요청자로 설정
                return JsonResponse(serializer.data,
                                    status=status.HTTP_201_CREATED)
            try:
                return Response(serializer.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
            except:
                return Response(form.errors,
                                status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(status=status.HTTP_401_UNAUTHORIZED)


class DoorlockDetail(generics.RetrieveUpdateAPIView):
    queryset = Doorlock.objects.all()
    serializer_class = DoorlockSerializer
    permission_classes = (permissions.IsAuthenticated, )


@swagger_auto_schema(method='post',
                     operation_description="Send open push to a doorlock",
                     responses={
                         200: 'Successfully did requested work',
                     })
@api_view(['POST'])
def send_open_push(request, beacon_id):
    # 계정의 accessible_beacon_id에 있을 경우
    # 해당 beacon_id와 같은 도어록을 갖고와서
    # 해당 도어록의 push_id를 갖고 push
    pass


@swagger_auto_schema(
    method='post',
    operation_description="Give permissions about doorlock to given user",
    responses={
        200: 'Successfully did requested work',
        400: 'Unauthorized',
        406: 'username not given to the post body data',
    },
    manual_parameters=DoorlockSerializer.Meta.parameters)
@api_view(['POST'])
def invite(request, beacon_id):
    doorlock = Doorlock.objects.filter(beacon_id=beacon_id)
    if (request.data.get('username') == None):
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE)
    if (doorlock.owner == request.user):
        invited_user = User.objects.filter(
            username=request.data.get('username'))
        profile = Profile.objects.filter(user=invited_user)
        accessible_beacons_id = json.load(profile.accessible_beacon_id)
        accessible_beacons_id.append(beacon_id)
        profile.accessible_beacon_id = json.dumps(accessible_beacons_id)
        profile.save()
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)