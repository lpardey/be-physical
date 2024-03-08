from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request

from .models import BearerToken


@api_view(["POST"])
def login(request: Request) -> JsonResponse:
    user = authenticate(username=request.POST["username"], password=request.POST["password"])

    if user is None:
        return JsonResponse({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    token, created = BearerToken.objects.get_or_create(user=user)

    return JsonResponse({"token": token.key})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout(request: Request) -> JsonResponse:
    try:
        token = request.auth
        token.delete()
        return JsonResponse({"detail": "Logout successful"}, status=status.HTTP_200_OK)

    except token.DoesNotExist as e:
        return JsonResponse({"detail": f"{e}"}, status=status.HTTP_400_BAD_REQUEST)
