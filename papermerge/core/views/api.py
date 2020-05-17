from django.http import Http404

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser, FileUploadParser)
from rest_framework.permissions import IsAuthenticated

from papermerge.core.models import (Document, BaseTreeNode)
from papermerge.core.serializers import DocumentSerializer


class PagesView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id):
        """
        Deletes Pages from doc_id document
        """
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Http404("Document does not exists")

        page_nums = request.GET.getlist('pages[]')
        page_nums = [int(number) for number in page_nums]

        doc.delete_pages(page_numbers=page_nums)

        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, doc_id):
        """
        Reorders pages from doc_id document
        """
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Http404("Document does not exists")

        doc.reorder_pages(request.data)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PagesCutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doc_id):
        """
        Cut Pages from doc_id document.
        It adds pages to clipboard designated for pages
        which where cut.
        """
        try:
            Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Http404("Document does not exists")

        page_nums = request.data
        page_nums = [int(number) for number in page_nums]

        # request.clipboard.pages.add(...)
        request.pages.add(doc_id=doc_id, page_nums=page_nums)

        return Response(status=status.HTTP_204_NO_CONTENT)


class PagesPasteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doc_id):
        """
        Paste pages (within document view).
        NO new document is created.
        Code for pasting document in changelist view (i.e. when
        a NEW document is created) is in
        papermerge.core.views.documents.paste_pages
        """
        before = request.POST.get('before', False)
        after = request.POST.get('after', False)

        try:
            document = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Http404("Document does not exists")

        Document.paste_pages(
            user=request.user,
            parent_id=document.parent,
            dst_document=document,
            doc_pages=request.pages.all(),
            before=before,
            after=after
        )

        request.pages.clear()

        return Response(status=status.HTTP_204_NO_CONTENT)


class DocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        documents = Document.objects.all()
        serializer = DocumentSerializer(documents, many=True)

        return Response(serializer.data)


class DocumentUploadView(APIView):
    """
    REST API for uploading a file.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def put(self, request, filename):
        file_obj = request.data['file']

        doc = Document.import_file(
            file_obj.temporary_file_path(),
            username=request.user.username,
            file_title=filename
        )

        if isinstance(doc, Document):
            serializer = DocumentSerializer(doc)
            return Response(serializer.data)

        return Response(status=200)


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
