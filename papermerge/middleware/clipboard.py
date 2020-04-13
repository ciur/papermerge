

class Clipboard:
    """
    Manages a clipboard of document and pages.
    Clipboard operates only with IDs (or page order numbers).

    Adds a clipboard attribute to request object.

    * Resets/Delets everything (for current user) from clipboard:

        request.clipboard.reset()

    * Get cliboard object for currently logged in user:

        request.clipboard.all()

    returns:

        {
            'nodes': ['node1', 'node2', 'node3'], # <- whole nodes to be pasted
            'pages': { # <- pages to be pasted (with their docs)
                'doc_id1': [page1, page2]
                'doc_id2': [page1]
            }
        }

    page1, page2, ... ARE PAGE ORDERs (page1 = 1 => first page)

    * Get current nodes in clipboard:

        request.clipboard.nodes.all()

    returns and array/list of node ids currently in clipboard

        ['node1', 'node2', ...]

    * Adds node ids into the clipboard. Node is a folder or a document's id:

        request.clipboard.nodes.add(1, 2, 3, 4)
        request.clipboard.nodes.add([1, 2, 3, 4])

    * Get pages currently in clipboard (for current user):

        request.cliboard.pages.all()

    returns:
        {
            'doc_id1': [page1, page2, page3],
            'doc_id2': [page1, page2, page3]
        }

        again, page1, page2 etc are page order numbers


    * Adds pages and their documents into the clipboard:

        request.clipboard.pages.add(1, [1, 2, 3])
        request.clipboard.pages.add(1, 1, 2, 3)

    first agrument is the document id. Rest of the arguments are
    page order numbers.

    Can be written as:

        request.clipboard.pages.add(doc=1, pages=[1, 2, 3])
        request.clipboard.pages.add(doc=1, page=2)

    """

    def __init__(self, get_response):

        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        return response
