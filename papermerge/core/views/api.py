from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from papermerge.core.models import Document
from papermerge.core.serializers import DocumentSerializer


# REST API
def documents(request):
    documents = Document.objects.all()
    serializer = DocumentSerializer(documents, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def document(request, pk):
    """
    Retrieve, update or delete a document.
    """
    try:
        document = Document.objects.get(pk=pk)
    except Document.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = DocumentSerializer(document)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = DocumentSerializer(document, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        Document.delete()
        return HttpResponse(status=204)
