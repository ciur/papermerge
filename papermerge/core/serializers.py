from rest_framework import serializers

from papermerge.core.models import (Document, User)


class UserSerializer(serializers.ModelSerializer):

    documents = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Document.objects.all()
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'documents']


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
        allow_null=True,
        max_length=100
    )
    page_count = serializers.IntegerField(
        read_only=True
    )

    user = serializers.ReadOnlyField(source='user.username')

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
