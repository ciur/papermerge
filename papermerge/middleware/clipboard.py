

class Clipboard:
    """
    Manages a clipboard of document and pages.

    Adds a clipboard attribute to request object.

    request.clipboard.


    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response
