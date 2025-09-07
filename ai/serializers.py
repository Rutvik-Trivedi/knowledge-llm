from rest_framework import serializers

from ai.models import StructuredInfo


class StructuredInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = StructuredInfo
        fields = [
            "id",
            "title",
            "summary",
            "sentiment",
            "topics",
            "keywords",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]
