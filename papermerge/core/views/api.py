from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser, FileUploadParser)
from rest_framework.permissions import IsAuthenticated

from papermerge.core.models import Document
from papermerge.core.serializers import DocumentSerializer


class DocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)

        return Response(serializer.data)


class DocumentUploadView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        file_obj = request.data['file']

        Document.import_file(
            file_obj.temporary_file_path(),
            username=request.user.username
        )

        return Response(status=204)


class DocumentView(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Document.objects.get(pk=pk)
        except Document.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        """
        Retrieve, update or delete a document.
        """
        document = self.get_object(pk)

        serializer = DocumentSerializer(document)

        return Response(serializer.data)

    def put(self, request, pk):
        data = JSONParser().parse(request)
        document = self.get_object(pk)

        serializer = DocumentSerializer(document, data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):

        document = self.get_object(pk)
        document.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
