from rest_framework import serializers

from papermerge.core.models import Document


class DocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )

    def create(self, validated_data):
        """
        Create and return a new `Document` instance, given the validated data.
        """
        return Document.objects.create(**validated_data)
