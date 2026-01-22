from rest_framework import serializers
from django.core.validators import RegexValidator


class FisherNicknameRequestSerializer(serializers.Serializer):
    nickname = serializers.CharField(
        max_length=30,
        validators=[
            RegexValidator(
                regex=r"^[A-Za-z0-9_]+$",
                message="Nickname can only contain letters, numbers, and underscores.",
            )
        ],
        trim_whitespace=True,
    )
