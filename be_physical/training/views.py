# from django.shortcuts import get_object_or_404
# from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from serializers import TrainingSerializer

from ..user_info.models import UserInfo
from .models import Training


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_training(request: Request) -> Response:
    user_info = get_object_or_404(UserInfo, user=request.user)
    trainings = Training.objects.filter(user_info=user_info)
    serializer = TrainingSerializer(trainings, many=True)
    response = Response(serializer.data)
    return response


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_workouts(request: Request) -> Response:
    return Response()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_exercises(request: Request) -> Response:
    return Response()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_streak(request: Request) -> Response:
    return Response()


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_training_goals(request: Request) -> Response:
    return Response()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_training(request: Request) -> Response:
    return Response()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_workout(request: Request) -> Response:
    return Response()


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_diet(request: Request) -> Response:
    return Response()
