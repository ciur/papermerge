from rest_framework import serializers

from papermerge.core.models import Document


class DocumentSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    notes = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=100
    )
    page_count = serializers.IntegerField(
        read_only=True
    )

    def update(self, instance, validated_data):
        """
        Update and return an existing `Document` instance,
        given the validated data.
        """
        instance.title = validated_data.get('title', instance.title)
        instance.notes = validated_data.get('notes', instance.notes)
        instance.save()

        return instance

    def create(self, validated_data):
        """
        Create and return a new `Document` instance, given the validated data.
        """
        return Document.objects.create(**validated_data)
