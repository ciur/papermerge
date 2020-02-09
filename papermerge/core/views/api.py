from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import (api_view, permission_classes)
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated

from papermerge.core.models import Document
from papermerge.core.serializers import DocumentSerializer


# REST API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)

    return Response(serializer.data)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def document(request, pk):
    """
    Retrieve, update or delete a document.
    """
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DocumentSerializer(document)

        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DocumentSerializer(document, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    elif request.method == 'DELETE':
        Document.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
