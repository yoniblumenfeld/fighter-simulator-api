from rest_framework.response import Response
from .models import UserProfile,Fighter
from . import serializers,permissions
from rest_framework import status,filters,viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
# Create your views here.

class ProfilesViewSet(viewsets.ModelViewSet):
    """
    Handles crud ops for profiles on our system
    Uses token authentication
    """
    serializer_class = serializers.UserProfileSerializer
    queryset = UserProfile.objects.all()
    permission_classes = (permissions.UpdateOwnProfile,)
    authentication_classes = (TokenAuthentication,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('email','name')

    def destroy(self, request, *args, **kwargs):
        """Returns status code 200 if deletion succeed"""
        super().destroy(self,request,*args,**kwargs)
        return Response(status=status.HTTP_200_OK)

class LoginViewSet(viewsets.ViewSet):
    """Checks email and password and return an auth token"""
    serializer_class = AuthTokenSerializer

    def create(self,request):
        """Use the ObtainAuthToken to validate and create a token"""
        return ObtainAuthToken().post(request)

class FighterViewSet(viewsets.ModelViewSet):
    """Handles crud ops for fighter objects"""
    permission_classes = (permissions.UpdateOwnFighter,)
    authentication_classes = (TokenAuthentication, )
    queryset = Fighter.objects.all()
    serializer_class = serializers.FighterSerializer

    def destroy(self, request, *args, **kwargs):
        """Returns status code 200 if deletion succeed"""
        super().destroy(self,request,*args,**kwargs)
        return Response(status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        serializer.save(user_profile=self.request.user)