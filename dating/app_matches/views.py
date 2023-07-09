from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .serializers import MatchSerializer
from services.user.user import UserInterface
from .permissions import IsLikeYourself

from rest_framework.views import APIView


class MatchAPIView(APIView):
    permission_classes = []
    serializer_class = MatchSerializer

    def get(self, request: Request, id: int) -> Response:

        user_data = UserInterface.get_user_data_for_match(id, request)

        if user_data:
            return Response(user_data, status=status.HTTP_200_OK)
        return Response({'message': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request, id: int) -> Response:
        like_type = request.data.get('like_type')

        if not like_type:
            return Response({'message': "Идем дальше?"}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(data=request.data, context={'sender_id': request.user.id, 'receiver_id': id})
        serializer.is_valid(raise_exception=True)
        flag, message = serializer.save()

        if flag:
            return Response({'message': message}, status=status.HTTP_201_CREATED)

        return Response({'message': message}, status=status.HTTP_400_BAD_REQUEST)

    def get_permissions(self):
        permissions = []
        if self.request.method == "POST":
            permissions = [IsAuthenticated, IsLikeYourself]
        return [permission() for permission in permissions]
