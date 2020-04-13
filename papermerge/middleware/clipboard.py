

class Clipboard:
    """
    Manages a clipboard of document and pages.

    Adds a clipboard attribute to request object.

    * Resets/Delets everything (for current user) from clipboard:

        request.clipboard.reset()

    * Get cliboard object for currently logged in user:

        request.clipboard

    * Puts node ids into the clipboard. Node might be a folder or a document

        request.clipboard.put(node_ids=[1, 2, 3, 4])

    * Puts page ids and their document id into the clipboard:

        request.clipboard.put(document_id=1, page_nums=[1, 2, 3])

    Achtung! page_nums are actual page order numbers (not their IDs), e.g.
    page_nums = [1, 2] are first and second pages of the associated document

    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response
