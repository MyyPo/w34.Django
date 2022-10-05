from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import exceptions


from .models import User

from .serializers import SaveSerializer, UserSerializer
from .services import create_fresh_save
from .utils import mail_builder


class StartNewGame(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = SaveSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        # try:
        serializer.instance = create_fresh_save(user=request.user, save=data)
        # except:
        #     raise exceptions.ValidationError(
        #         {"detail": _("You can't have several saves with the same name")}
        #     )
        return Response(data=serializer.data)


class RegisterAPI(CreateAPIView):
    permission_classes = [AllowAny]
    model = get_user_model()
    serializer_class = UserSerializer


class GetUserSelfAPI(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)


class VerifyEmailAPI(GenericAPIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if request.user.verified_email is True:
            raise Exception(_("Email address already verified"))
        if request.user.email != request.user.new_email:
            raise Exception(_("Unable to verify this email address"))
        email = mail_builder.send_verification(request.user, {"user": request.user})
        email.send()
        return Response(status=200, data=_("Verification email has been sent"))
