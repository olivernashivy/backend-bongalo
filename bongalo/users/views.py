from rest_framework import generics, permissions, mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from knox.models import AuthToken
from .serializer import UserSerializer, RegisterSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.models import AuthToken
from django.contrib.auth import login
from .models import User
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)

class UserViewSet(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def send_verification_code(self, request, *args, **kwargs):
        """Trigger a one-time-password to be emailed to a user.
        The code will be used to set (or reset) the password on the user."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            'Email sent.',
            status=status.HTTP_201_CREATED,
        )
    def deactivate_account(self, request, *args, **kwargs):
        request.user.is_active = False
        request.user.save()
        return Response(
            'User deactivated.',
            status=status.HTTP_200_OK,
        )


    @action(methods=['get', 'put', 'patch'], detail=False)
    def me(self, request, *args, **kwargs):
        if request.method == 'GET':
            return Response(self.get_serializer(request.user).data)
        else:
            self.kwargs[self.lookup_url_kwarg or self.lookup_field] = request.user.pk
            return super().update(request, *args, **kwargs)