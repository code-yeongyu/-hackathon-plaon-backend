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


class ArticleDetail(generics.RetrieveUpdateAPIView):
    queryset = Doorlock.objects.all()
    serializer_class = DoorlockSerializer
    permission_classes = (permissions.IsAuthenticated, )
