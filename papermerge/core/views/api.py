from django.http import Http404
from django.utils.translation import gettext as _

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.parsers import (JSONParser, FileUploadParser)
from rest_framework.permissions import IsAuthenticated

from papermerge.core.models import (
    Document, Access
)
from papermerge.core.serializers import DocumentSerializer
from papermerge.core.document_importer import DocumentImporter


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

        if request.user.has_perm(
            Access.PERM_WRITE, doc
        ):
            page_nums = request.GET.getlist('pages[]')
            page_nums = [int(number) for number in page_nums]

            doc.delete_pages(page_numbers=page_nums)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request, doc_id):
        """
        Reorders pages from doc_id document

        request.data is expected to be a list of dictionaries:
        Example:
            [
                {page_num: 2, page_order: 1},
                {page_num: 1, page_order: 2},
                {page_num: 3, page_order: 3}
            ]
        which reads:
            page number 2, must become page number 1
            page number 1, must become page number 2
            page number 3 stays same.
        """
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Http404("Document does not exists")

        if request.user.has_perm(
            Access.PERM_WRITE, doc
        ):
            doc.reorder_pages(request.data)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_403_FORBIDDEN)


class PagesCutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, doc_id):
        """
        Cut Pages from doc_id document.
        It adds pages to clipboard designated for pages
        which where cut.
        """
        try:
            doc = Document.objects.get(id=doc_id)
        except Document.DoesNotExist:
            raise Http404("Document does not exists")

        if request.user.has_perm(
            Access.PERM_WRITE, doc
        ):
            page_nums = request.data
            page_nums = [int(number) for number in page_nums]

            # request.clipboard.pages.add(...)
            request.pages.add(doc_id=doc_id, page_nums=page_nums)

            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={
                'msg': _(
                    "You don't have permissions to cut pages"
                    " in this document."
                )
            }
        )


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

        if request.user.has_perm(
            Access.PERM_WRITE, document
        ):
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

        return Response(
            status=status.HTTP_403_FORBIDDEN,
            data={
                'msg': _(
                    "You don't have permissions to paste pages"
                    " in this document."
                )
            }
        )


class DocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        docs_list = []
        docs = Document.objects.all()

        docs_perms = request.user.get_perms_dict(
            docs, Access.ALL_PERMS
        )

        for doc in docs:
            if docs_perms[doc.id].get(Access.PERM_READ, False):
                doc_dict = doc.to_dict()
                docs_list.append(
                    doc_dict
                )

        return Response(docs_list)


class DocumentUploadView(APIView):
    """
    REST API for uploading a file.
    """
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def put(self, request, filename):
        file_obj = request.data['file']
        imp = DocumentImporter(
            file=file_obj.temporary_file_path(),
            username=request.user.username,
        )
        doc = imp.import_file(
            file_title=filename,
            apply_async=True,
            delete_after_import=False
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

        if request.user.has_perm(Access.PERM_READ, document):
            serializer = DocumentSerializer(document)
            return Response(serializer.data)

        return Response(
            status=status.HTTP_403_FORBIDDEN
        )

    def put(self, request, pk):
        data = JSONParser().parse(request)
        document = self.get_object(pk)

        if request.user.has_perm(Access.PERM_WRITE, document):
            serializer = DocumentSerializer(document, data=data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

        return Response(
            status=status.HTTP_403_FORBIDDEN
        )

    def delete(self, request, pk):

        document = self.get_object(pk)

        if request.user.has_perm(Access.PERM_DELETE, document):
            document.delete()
            return Response(status=status.HTTP_200_OK)

        return Response(
            status=status.HTTP_403_FORBIDDEN
        )
