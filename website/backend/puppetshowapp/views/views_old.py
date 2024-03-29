from django.http import HttpResponse, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from ..models import Outfit, Scene, DiscordPointingUser, DiscordData
from ..serializers import (
    OutfitSerializer,
    SceneSerializer,
    DiscordDataSerializer,
    UserSerializer,
)
from ..permissions import IsObjectOwner, UserIsUser
from rest_framework import viewsets, permissions, status, generics, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from ..secrets.constants import (
    DISCORD_CLIENT_ID,
    DISCORD_CLIENT_SECRET,
    DISCORD_CALLBACK,
)
from django.shortcuts import redirect
from social_django.utils import load_strategy
from social_core.exceptions import AuthTokenError
from social_core.backends.discord import DiscordOAuth2
from social_django.utils import psa
from social_django.models import UserSocialAuth
from django.views.generic.base import View
from django.shortcuts import render

# DELETE IN PRODUCTION
import os

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


# Root
@api_view(["GET"])
def api_root(request, format=None):
    # TODO this should not be list, this should be a bunch of other functions
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "users-create": reverse("user-create", request=request, format=format),
            "scene": reverse("scene-create", request=request, format=format),
            "scene-detail": reverse("scene-detail", request=request, format=format),
            # "actors": reverse("actors-list", request=request, format=format),
            # "data": reverse("data-list", request=request, format=format),
        }
    )


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


def test_success(request):
    return HttpResponse("You have done it.")


#################################################
# Discord Redirect
#################################################
# def discord_login(request):
#     oauth = OAuth2Session(
#         DISCORD_CLIENT_ID,
#         redirect_uri=DISCORD_REDIRECT_URI,
#         scope=["email", "guilds.members.read", "identify"],
#     )
#     authorization_url, state = oauth.authorization_url(
#         "https://discord.com/api/oauth2/authorize"
#     )
#     return redirect(authorization_url)


# def discord_callback(request):
#     oauth = OAuth2Session(
#         DISCORD_CLIENT_ID,
#         redirect_uri=DISCORD_REDIRECT_URI,
#         scope=["identify", "email", "guilds.members.read"],
#     )
#     token = oauth.fetch_token(
#         "https://discord.com/api/oauth2/token",
#         authorization_response=request.build_absolute_uri(),
#         client_secret=DISCORD_CLIENT_SECRET,
#     )
#     request.session["discord_token"] = token
#     user_data = oauth.get("https://discord.com/api/users/@me")
#     discord_data = DiscordData.objects.get_or_create(user_snowflake=user_data)

#     return redirect(secret_page)


#################################################
# User API functions
#################################################


class UserList(generics.ListAPIView):
    permission_classes = [UserIsUser]
    queryset = DiscordPointingUser.objects.all()
    serializer_class = UserSerializer


class UserCreate(generics.CreateAPIView):
    permission_classes = [UserIsUser]
    queryset = DiscordPointingUser.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    permission_classes = [UserIsUser]
    queryset = DiscordPointingUser.objects.all()
    serializer_class = UserSerializer


#################################################
# Scene API Functions
#################################################


class SceneList(generics.ListCreateAPIView):
    permission_classes = [IsObjectOwner]
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer

    def perform_create(self, serializer):
        serializer.save(scene_author=self.request.user)


class SceneDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsObjectOwner]
    queryset = Scene.objects.all()
    serializer_class = SceneSerializer


#################################################
# Actor API functions
#################################################


class ActorCreate(generics.CreateAPIView):
    permission_classes = [IsObjectOwner]
    queryset = Scene.objects.all()
    serializer_class = OutfitSerializer


class ActorDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsObjectOwner]
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer


#################################################
# Debug only
#################################################


# def secret_page(request, *args, **kwargs):
#     try:
#         oauth = OAuth2Session(
#             DISCORD_CLIENT_ID,
#             token=request.session["discord_token"],
#         )
#     except KeyError:
#         return redirect(discord_login)
#     user = oauth.get("https://discord.com/api/users/@me").json()
#     return JsonResponse(user)


#################################################
# Testing: Discord info request
#################################################
def discord_user_info(request):
    user = request.user
    strategy = load_strategy(request)
    try:
        discord = user.social_auth.get(provider="discord")
    except AuthTokenError:
        return status.HTTP_400_BAD_REQUEST
    data = discord.get_json("/users/@me")
    username = data
