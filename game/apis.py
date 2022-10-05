from rest_framework import views
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from users.serializers import SaveSerializer
from game.serializers import GameSerializer
from game.serializers import SceneSerializer
from game.models import Scene, GameSave
from game.services import play, get_save


class Game(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = play(user=request.user, choice=request.data)
        serializer = GameSerializer(data, many=True)
        return Response(data=serializer.data)

    def get(self, request):
        data = get_save(user=request.user, data=request.data)
        serializer = GameSerializer(data, many=True)
        return Response(data=serializer.data)


class GetScenesAPI(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SceneSerializer
    queryset = Scene.objects.all()


# class GetScenesAPI(views.APIView):
#     permission_classes = [AllowAny]

#     def get(self, request):
#         serializer = SceneSerializer()

#         return Response(serializer.data)
