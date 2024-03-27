from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from .models import BearerToken


@api_view(["POST"])
def login(request: Request) -> Response:
    user = authenticate(username=request.data.get("username"), password=request.data.get("password"))

    if user is None:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = BearerToken.objects.get_or_create(user=user)
    return Response({"token": token.key})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> Response:
    try:
        token = request.auth
        token.delete()
        return Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)

    except token.DoesNotExist as e:
        return Response({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
