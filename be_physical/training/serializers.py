from rest_framework import serializers

from .models import Training


class TrainingSerializer(serializers.ModelSerializer[Training]):
    class Meta:
        model = Training
        exclude = ["user_info"]
